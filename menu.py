from flask import safe_join
from functools import wraps
import os

from OrderedDefaultdict import OrderedDefaultdict

global_menu = OrderedDefaultdict(OrderedDefaultdict)

no_flask_login = True

def init_app(app):
    @app.template_global('issubmenu')
    def issubmenu(value):
        # print "is", isinstance(value, OrderedDefaultdict), "type", type(value), "val", value
        return isinstance(value, OrderedDefaultdict)
    if no_flask_login:
        class fake_user(object):
            id = 1
            is_super = True
            @staticmethod
            def is_authenticated():
                return True

        def user_context_processor():
                return dict(current_user=fake_user)

        app.context_processor(user_context_processor)


def add_menu(row_text, col_text, route, blueprint=None, submenu=None):
    if blueprint:
        route = os.path.join('/', safe_join(blueprint.name, route))
    if submenu:
        if row_text in global_menu and col_text in global_menu[row_text]:
            if not isinstance(global_menu[row_text][col_text], OrderedDefaultdict):
                print "not ordered dict, not adding"
            else:
                global_menu[row_text][col_text][submenu] = route
        else:
            global_menu[row_text][col_text] = OrderedDefaultdict(str)
            global_menu[row_text][col_text][submenu] = route
    else:
        global_menu[row_text][col_text] = route

    @wraps
    def deco(f):
        return f
    return deco
