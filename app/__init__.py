from flask import Flask
from config import configs

def create_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config])

    return app