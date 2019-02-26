from . import blog
from model import getSessionFactory, Articles, Categories, Comments
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
    if not article:
        session.close()
        abort(404)

    data = article.get_map_data()
    session.close()

    return jsonify(data)


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
    data = request.json

    username = data.get('username', None)
    email = data.get('email', None)
    content = data.get('content', None)
    comment_type = 0

    if not username or not content:
        abort(400, 'bad request')
    
    session_factory = getSessionFactory()
    session = session_factory.get_session()
    new_comment = Comments(username, email, None, content, post_id, comment_type, None)
    session.add(new_comment)
    session.commit()
    session.close()

    return jsonify({'ret': True})


@blog.route('/post/<int:post_id>/comment/<int:comment_id>/comment', methods=['POST'])
def comment_comment(post_id, comment_id):
    data = request.json

    username = data.get('username', None)
    email = data.get('email', None)
    content = data.get('content', None)
    comment_type = 1

    if not username or not content:
        abort(400, 'bad request')
    
    session_factory = getSessionFactory()
    session = session_factory.get_session()
    new_comment = Comments(username, email, None, content, post_id, comment_type, comment_id)
    session.add(new_comment)
    session.commit()
    session.close()

    return jsonify({'ret': True})
