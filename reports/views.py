import datetime
import json
import decimal
from flask import Blueprint, render_template, request, g, Response

from sqlalchemy import func

from sql_errors import catch_sql_errors
from schema import Radacct, metadata
from menu import add_menu
from dtables.dtorm import DTable, DTColumn
from dtables.funs import vhandler

reports = Blueprint('reports', __name__, template_folder='templates')


def sg(obj):
    if isinstance(obj, datetime.date):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))

render_decimal = """function (data, type, full, meta) {
                        return filesize(data);
                   }"""


class UsageDTable(DTable):
    radacct__radacctid = DTColumn('id', hidden=True, sortable=False)
    radacct__username = DTColumn('User Name')
    radacct__total = DTColumn('Total', render=render_decimal)
    radacct__acctsessiontime = DTColumn('Time', sort_column=[1, 'desc'])
    radacct__acctstarttime = DTColumn('Start')

    @classmethod
    def dt_item_id(self, item):
        return str(item.radacct__radacctid)


@reports.route('/usagedt_data/')
def usagedt_data():
    qry = None
    if 'sParams' in request.args:
        params = dict(ii.split('=') for ii in request.args['sParams'].split('|'))
    else:
        params = dict()
    if 'agg' in params and params['agg'] == 'sum':
        qry = g.session.query(
            func.min(Radacct.acctstarttime).label('radacct__acctstarttime'),
            func.sum(Radacct.acctinputoctets + Radacct.acctoutputoctets).label('radacct__total'),
            func.sum(Radacct.acctsessiontime).label('radacct__acctsessiontime'))\
                        .group_by(Radacct.username, Radacct.callingstationid)
    else:
        qry = g.session.query((Radacct.acctinputoctets + Radacct.acctoutputoctets).label('radacct__total'))

    if 'period' in params:
        days = int(params['period'])
    else:
        days = 30
    qry = qry.filter(Radacct.acctstarttime >
                datetime.datetime.now() -
                datetime.timedelta(days=days))
    results = vhandler(qry, metadata, dtable=UsageDTable)
    return Response(json.dumps(results, default=sg), mimetype='application/json')


@add_menu('Reports', 'Usage DT', 'usagedt', reports)
@add_menu('Reports', 'Usage DT Sum', 'usagedt?filter=agg=sum', reports)
@add_menu('Reports', 'Usage DT for 10 days', 'usagedt?filter=agg=sum|period=10', reports)
@reports.route('/usagedt')
@catch_sql_errors('login')
def usagedt():
    filter = request.args.get('filter', None)
    return render_template('usagedt.html', dtable=UsageDTable, filter=filter)
