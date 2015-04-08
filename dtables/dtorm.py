import inspect


class DTColumn(object):
    creation_counter = 0

    def __init__(self, title='', **kwargs):
        self.creation_order = DTColumn.creation_counter
        DTColumn.creation_counter += 1
        self.title = title
        self.options = dict(kwargs)

    def __getattr__(self, entry):
        return self.options.get(entry, None)

class ListingMeta(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        cls.columns = sorted(inspect.getmembers(cls, lambda o: isinstance(o, DTColumn)), key=lambda i: i[1].creation_order)
        cls.nb_columns = len(cls.columns)
        return cls


# classmethods because we don't ever instantiate a live instance of the class. Good/bad?
class DTable(object):
    __metaclass__ = ListingMeta

    @classmethod
    def dt_data_columns(self):
        return [colname for colname, col in self.columns if not col.calculated]

    @classmethod
    def dt_columns(self):
        dblock = "[\n"
        for colname, col in self.columns:
            dblock += '{ title: "%s", ' % col.title
            dblock += 'name: "%s", ' % colname
            # if not col.calculated:
            dblock += 'mData: "%s", ' % colname
            if col.render:
                dblock += 'mRender: %s, ' % col.render
            if col.sortable == None:
                dblock += 'orderable: true, '
            else:
                dblock += 'orderable: false, '
            if col.hidden:
                dblock += '"visible": false, '
            dblock += '},\n'
        dblock += "]"
        return dblock

    @classmethod
    def dt_order_info(self):
        sorder = [(ii, aa.sort_column[1]) for ii, (cr, aa) in enumerate(self.columns) if aa.sort_column]
        return '[' + ', '.join("[%d, '%s']" % (ii[0], ii[1]) for ii in sorder) + ']'

    @classmethod
    def dt_map_columns(self, item):
        ff = dict()
        for colname, col in self.columns:
            if col.calculated:
                continue
            try:
                value = item[colname]
                rdata = col.mapper(value) if col.mapper else value
            except Exception as ee:
                print "col name", colname, "not in ", item, "error", str(ee)
                from IPython import embed; embed()

            ff[colname] = rdata if rdata is not None else ''
        return ff

    @classmethod
    def dt_item_id(self, item):
        return item.id



if __name__ == '__main__':
    class UsersDTable(DTable):
        id = DTColumn('Id')
        email = DTColumn('Email')
        first_name = DTColumn('First Name')
        last_name = DTColumn('Last Name')

    vs = UsersDTable()
