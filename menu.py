from flask import safe_join
from functools import wraps
import os

from OrderedDefaultdict import OrderedDefaultdict

global_menu = OrderedDefaultdict(OrderedDefaultdict)


def add_menu(row_text, col_text, route, blueprint=None):
    if blueprint:
        route = os.path.join('/', safe_join(blueprint.name, route))
    global_menu[row_text][col_text] = route

    @wraps
    def deco(f):
        return f
    return deco
