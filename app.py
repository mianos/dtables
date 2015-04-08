#!/usr/bin/env python
import sys
import time
from flask import Flask, redirect, url_for, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import configobj
import jinja_local.jinja_filters

import reports


def create_app():
    app = Flask(__name__)
#    app.config['STATIC_RESOURCES'] = True
    app.secret_key = "\xca\xcf\x16O\x04\x47\x0eFN\xf9\x0c,\xfb4{''<\x9b\xfc\x08\x87\xe9\x13"

    app.settings = configobj.ConfigObj('settings.ini')

    engine = create_engine(app.settings['database']['connection'], echo=True, pool_recycle=3600)
    Session = sessionmaker(bind=engine)  # autocommit=True)

    jinja_local.jinja_filters.init_app(app)
    app.register_blueprint(reports.reports, url_prefix='/reports')

    @app.route('/')
    def root():
        return redirect(url_for('reports.usagedt'))

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
