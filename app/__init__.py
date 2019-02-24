from flask import Flask
from config import configs
from .backend import blog

def create_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config])

    app.register_blueprint(blog)

    return app