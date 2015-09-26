import datetime
import json
import decimal
from flask import Blueprint, render_template, request, g, Response, url_for

from sqlalchemy import func

from sql_errors import catch_sql_errors
from schema import User, metadata
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


class UsersDTable(DTable):
    es_users__id = DTColumn('id', hidden=True, sortable=False)
    es_users__email = DTColumn()
    es_users__first_name = DTColumn()
    es_users__last_name = DTColumn()

    @classmethod
    def dt_item_id(self, item):
        return str(item.es_users__id)


@reports.route('/usagedt_data')
def list_data():
    qry = g.session.query(User)

    results = vhandler(qry, metadata.tables, dtable=UsersDTable)
    return Response(json.dumps(results, default=sg), mimetype='application/json')


@add_menu('Users', 'List', 'users_list', reports)
@reports.route('/users_list')
@catch_sql_errors('login')
def users_list():
    return render_template('generic_report.html',
                           dtable=UsersDTable,
                           get_data=url_for('reports.list_data', what=None),
                           title='Users')
