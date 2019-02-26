from . import blog
from model import getSessionFactory, Articles, Categories
from flask import render_template, redirect, url_for, abort, current_app, request, abort, jsonify
from utils import get_page
from sqlalchemy.orm.session import Session


@blog.route('/posts', methods=['GET'])
def get_articles():
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)

    session = getSessionFactory().get_session()
    articles = session.query(Articles).order_by(
        Articles.id).offset(offset).limit(limit).all()

    datas = []
    for article in articles:
        datas.append(article.get_map_data())
    
    session.close()

    return jsonify({'datas': datas, 'pager': {'page': page, 'size': size}})


@blog.route('/post/<int:post_id>', methods=['GET'])
def get_article(post_id):
    session = getSessionFactory().get_session()
    article = session.query(Articles).filter(Articles.id == post_id).first()
    session.close()

    if not article:
        abort(404)
    return jsonify(article.get_map_data())


@blog.route('/categories', methods=['GET'])
def get_categories():
    session = getSessionFactory().get_session()
    categories = session.query(Categories).order_by(Categories.id).all()
    session.close()

    datas = []
    for category in categories:
        datas.append(category.get_map_data())

    return jsonify({'datas': datas})


@blog.route('/category/<int:category_id>/posts', methods=['GET'])
def get_articles_by_category(category_id):
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)

    session = getSessionFactory().get_session()
    articles = session.query(Articles).filter(Articles.category_id == category_id).order_by(
        Articles.id).offset(offset).limit(limit).all()
    session.close()

    datas = []
    for article in articles:
        datas.append(article.get_map_data())

    return jsonify({'datas': datas, 'pager': {'page': page, 'size': size}})


@blog.route('/post/<int:post_id>/comment', methods=['POST'])
def comment_post(post_id):
    
