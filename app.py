from app import create_app
from admin import create_admin_app
from flaskext.markdown import Markdown
from datetime import datetime
from flask import current_app
from os import environ

app = create_app(environ.get('ENV', 'dev'))
admin_app = create_admin_app(environ.get('ENV', 'dev'))
Markdown(app)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_power():
    return {'power': current_app.config['POWERD']}

@app.context_processor
def inject_beian():
    return {'beian': current_app.config['BEIAN']}
