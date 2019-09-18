from app import create_app
from os import environ

app = create_app(environ.get('ENV', 'dev'))
