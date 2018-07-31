from flask import Flask
from config import configs
from .main import main

def create_admin_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config])

    app.register_blueprint(main)

    return app
