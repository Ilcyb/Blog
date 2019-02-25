from flask import Flask
from config import configs
from .blog.backend import blog
from .admin.backend import admin

def create_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config])

    app.register_blueprint(blog, url_prefix='/blog/api')
    app.register_blueprint(admin, url_prefix='/admin/api')

    return app