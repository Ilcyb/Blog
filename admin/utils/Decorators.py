from flask import session, url_for, redirect
from functools import wraps

def login_required(func):
    @wraps(func)
    def handle_args(*args, **kwargs):
        if session.get('is_admin', None) == True:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main.login'))
    return handle_args