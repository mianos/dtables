#!/usr/bin/env python
import sys
from flask import Flask, redirect, url_for, g, Blueprint, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import configobj
import jinja_local.jinja_filters

import reports
import menu

# some stubs because flask_login is not used. Delete these and add flask login
auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    flash('login ROFL')
    return redirect(url_for('reports.users_list'))


@auth.route('/logout')
def logout():
    flash('logout ROFL')
    return redirect(url_for('reports.users_list'))


def create_app():
    app = Flask(__name__)
#    app.config['STATIC_RESOURCES'] = True
    app.secret_key = "\xca\xcf\x16O\x04\x47\x0eFN\xf9\x0c,\xfb4{''<\x9b\xfc\x08\x87\xe9\x13"

    app.settings = configobj.ConfigObj('settings.ini')

    engine = create_engine(app.settings['database']['connection'], echo=True, pool_recycle=3600)
    Session = sessionmaker(bind=engine)  # autocommit=True)

    menu.init_app(app)
    jinja_local.jinja_filters.init_app(app)
    app.register_blueprint(reports.reports, url_prefix='/reports')
    app.register_blueprint(auth)

    @app.route('/')
    def root():
        return redirect(url_for('reports.users_list'))

    @app.after_request
    def session_commit(response):
        session = getattr(g, 'session', None)
        if session is not None:
            g.session.commit()
        return response

    @app.before_request
    def before_request():
        g.session = Session()

    @app.teardown_request
    def teardown_request(exception):
        session = getattr(g, 'session', None)
        if session is not None:
            session.close()
    return app

app = create_app()

if __name__ == '__main__':
    if sys.platform == 'darwin':
        host = 'localhost'
    else:
        host = '0.0.0.0'
    app.run(debug=True, port=8080, host=host)
