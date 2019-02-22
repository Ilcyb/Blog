from flask import session, url_for, redirect
from functools import wraps

def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

def login_required(func):
    @wraps(func)
    def handle_args(*args, **kwargs):
        if session.get('is_admin', None) == True:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main.login'))
    return handle_args