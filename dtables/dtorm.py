import inspect


class DTColumn(object):
    creation_counter = 0

    def __init__(self, title=None, **kwargs):
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

jsstr = repr


class DTableColumnHandlers:
    def title(colname, col):
        if col.title:
            title = col.title
        else:
            if '__' in colname:
                title = colname.split('__')[1].replace('_', ' ')
            else:
                title = colname.replace('_', ' ')
        return jsstr(title)

    def name(colname, col):
        return jsstr(colname)

    def mData(colname, col):
        return jsstr(colname)

    def mRender(colname, col):
        return col.render(colname, col) if col.render else None

    def orderable(colname, col):
        return jsstr('true') if col.sortable is None else jsstr('false')

    def hidden(colname, col):
        return jsstr('false') if col.hidden else None


# classmethods because we don't ever instantiate a live instance of the class. Good/bad?
class DTable(object):
    __metaclass__ = ListingMeta

    @classmethod
    def dt_data_columns(self):
        return [colname for colname, col in self.columns if not col.calculated]

    @classmethod
    def dt_columns(self):
        rowlist = list()
        for colname, col in self.columns:
            column_list = list()
            for name, method in DTableColumnHandlers.__dict__.iteritems():
                if not callable(method):
                    continue
                value = method(colname, col)
                if value:
                    column_list.append("\t%s: %s" % (name, value))
            rowlist.append('{' + ",\n".join(column_list) + '}')
        return '[' + ',\n'.join(rowlist) + ']'

    @classmethod
    def dt_fixed_columns(self):
        for ii, (cr, aa) in enumerate(self.columns):
            if not aa.hidden and not aa.fixed:
                break
        if ii < len(self.columns):
            return ii
        else:
            return 0

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
                continue
                # from IPython import embed; embed()

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
