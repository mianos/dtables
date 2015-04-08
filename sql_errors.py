from functools import wraps

from flask import flash, redirect, url_for
import sqlalchemy.exc


def catch_sql_errors(route_to_on_error):
    def _second(target):
        @wraps(target)
        def _inner(*args, **kwargs):
            try:
                result = target(*args, **kwargs)
            except sqlalchemy.exc.OperationalError:
                flash("operational error, database does not exist or something", category='danger')
                return redirect(url_for(route_to_on_error))
            except sqlalchemy.exc.IntegrityError:
                flash("integrity error, ie keys duplicated etc", category='danger')
                return redirect(url_for(route_to_on_error))
            return result
        return _inner
    return _second
