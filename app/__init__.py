from flask import Flask
from config import configs
from .blog import blog
from .admin import admin

def create_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config])

    app.register_blueprint(blog)
    app.register_blueprint(admin, prefix='/admin')

    return app