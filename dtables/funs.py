import logging
from flask import request


logger = logging.getLogger(__name__)

def vhandler(query, all_tables, dtable, manual_map=False, count=None):
    # initialise the reply with the draw item from the request as datatables wants it back
    reply = dict(draw=int(request.args['draw']), data=[])
    if manual_map is not True:
        columns = list()
        column_names = list()
        for col in dtable.dt_data_columns():
            if '__' in col:
                table, column = col.split('__')
                if column not in all_tables[table].columns:
                    logger.error("Column missing, check metadata.tables[table].columns")
                    continue
                columns.append(all_tables[table].columns[column])
                column_names.append(col)
            else:
                # no table name, underlying expression column or something else aliased
                # so don't add the column and assume the developer puts it somewhere in the query
                continue

        existing_query_columns = set(ii['name'] for ii in query.column_descriptions)
        for col, name in zip(columns, column_names):
            if name in existing_query_columns:
                continue
            query = query.add_columns(col.label(name))

    sortCol = request.args.get('sortCol', None)
    if sortCol:
        scol = dtable.columns[int(sortCol)]
        col = next(dd['expr'] for dd in query.column_descriptions if dd['name'] == scol[0])
        if request.args.get('sortDir', 'asc') == 'desc':
            query = query.order_by(col.expression.desc())
        else:
            query = query.order_by(col.expression)
    else:
        for cname, dtcol in dtable.columns:
            if 'hidden' not in dtcol.options:
                for dd in query.column_descriptions:
                    if dd['name'] == cname:
                        col = dd['expr']
                        break
                else:
                    logger.error("Column %s 'missing' - class fields are of the form <table>__<field> where __ is a double underscore" % cname)
                    continue
                if request.args.get('sortDir', 'asc') == 'desc':
                    query = query.order_by(col.desc())
                else:
                    query = query.order_by(col.asc())
                break

    reply['recordsTotal'] = count if count else query.count()
    reply['recordsFiltered'] = reply['recordsTotal']

    items = query.offset(int(request.args['start']))

    if 'length' in request.args:
        try:
            ll = int(request.args['length'])
            if ll > 0:
                items = items.limit(ll)
        except ValueError:
            pass
        

    item_data = list()
    for item in items:
        ff = dtable.dt_map_columns(item._asdict())
        item_id = str(dtable.dt_item_id(item))
        ff['DT_RowId'] = item_id
        ff['DT_RowData'] = dict(pkey=item_id)
        item_data.append(ff)
    reply['data'] = item_data
    return reply
