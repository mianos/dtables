from flask import request


def vhandler(query, metadata, dtable):  # Add sqlalchemy filters here ... , **filters):
    # initialise the reply with the draw item from the request as datatables wants it back
    reply = dict(draw=int(request.args['draw']), data=[])
    columns = list()
    column_names = list()
    for col in dtable.dt_data_columns():
        if '__' in col:
            table, column = col.split('__')
            if column not in metadata.tables[table].columns:
                print "Column missing, check metadata.tables[table].columns"
                continue
            columns.append(metadata.tables[table].columns[column])
            column_names.append(col)
        else:
            print "table def not supportedf for column", col
            return

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

    reply['recordsTotal'] = query.count()
    reply['recordsFiltered'] = reply['recordsTotal']

    items = query.offset(int(request.args['start'])) \
                 .limit(int(request.args['length']))

    item_data = list()
    for item in items:
        ff = dtable.dt_map_columns(item._asdict())
        item_id = str(dtable.dt_item_id(item))
        ff['DT_RowId'] = item_id
        ff['DT_RowData'] = dict(pkey=item_id)
        item_data.append(ff)
    reply['data'] = item_data
    return reply
