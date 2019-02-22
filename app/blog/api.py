from . import blog
from model import PyMySqlSessionFactory, Articles
from flask import render_template, redirect, url_for, abort, current_app, request, abort
from sqlalchemy.orm.session import Session

session_factory = PyMySqlSessionFactory(
    current_app.config['MYSQL_USERNAME'],
    current_app.config['MYSQL_PASSWORD'],
    current_app.config['MYSQL_HOST'],
    int(current_app.config['MYSQL_PORT']),
    current_app.config['BLOG_DATABASE']
)


@blog.route('/articles', methods=['GET'])
def get_articles():

    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', 10))

    if page <= 0 or size <= 0:
        abort(400)

    session = session_factory.get_session()
    session.query(Articles)
