from flask import current_app, request, abort, Request, jsonify, make_response, Response
from model import getSessionFactory, Articles, Categories, Tags, Admin
from functools import wraps
from utils import enctry_string, dectry_string, get_page
from . import main
import json


def login_required(func):
    @wraps(func)
    def handle_args(*args, **kwargs):
        user_id = request.cookies.get('user_id', None)
        username = request.cookies.get('username', None)

        if not user_id or not username:
            abort(401, 'unauthorized')

        sessionFactory = getSessionFactory()
        query_session = sessionFactory.get_session()

        user = query_session.query(Admin).filter(
            Admin.id == int(user_id), Admin.username == username).first()

        if user is None:
            abort(401, 'unauthorized')

        return func(*args, **kwargs)

    return handle_args


@main.route('/loginStatus', methods=['GET'])
def get_login_status():
    user_id = request.cookies.get('user_id', None)
    username = request.cookies.get('username', None)

    if not user_id or not username:
        return jsonify({'status': False})

    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()

    user = session.query(Admin).filter(
        Admin.id == int(user_id), Admin.username == username).first()

    if user is None:
        return jsonify({'status': False})

    return jsonify({'status': True})


@main.route('/loginStatus', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400, 'bad request')

    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()

    user = session.query(Admin).filter(
        Admin.username == username, Admin.password == password).first()

    if user is None:
        abort(401, 'wrong password')

    resp = make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.body = json.dumps({'msg': 'ok'})
    resp.status_code = 200
    resp.set_cookie('user_id', 
                    str(user.id),
                    max_age=current_app.config['COOKIE_EXPIRE'])
    resp.set_cookie('username', 
                    user.username,
                    max_age=current_app.config['COOKIE_EXPIRE'])

    return resp


@main.route('/loginStatus', methods=['DELETE'])
def logout():
    resp = make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.body = json.dumps({'msg': 'ok'})
    resp.status_code = 200
    resp.delete_cookie('user_id')
    resp.delete_cookie('username')

    return resp


@main.route('/posts', methods=['GET'])
@login_required
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

    return jsonify({'datas': datas, 'pager': {'page': page, 'size': size}})


@main.route('/post/<int:post_id>', methods=['GET'])
@login_required
def get_article(post_id):
    session = getSessionFactory().get_session()
    article = session.query(Articles).filter(Articles.id == post_id).first()
    if not article:
        abort(404)
    return jsonify(article.get_map_data())


@main.route('/post', methods=['POST'])
@login_required
def create_article():
    data = request.json

    title = data.get('title', None)
    content = data.get('content', None)
    time = data.get('time', None)
    category = data.get('category_id', None)
    tags = data.get('tags', None)

    if not title or not content or not category:
        abort(400, 'invalid request')

    session = getSessionFactory().get_session()

    article = Articles(title, content, time, 0, category)
    session.add(article)

    for tag in tags:
        this_tag = session.query(Tags).filter(Tags.name == tag).first()
        if not this_tag:
            this_tag = Tags(tag)
        this_tag.articles.append(article)
        session.add(this_tag)

    session.commit()

    return jsonify({'msg': 'ok'})


@main.route('/post/<int:post_id>', methods=['PUT'])
@login_required
def update_article(post_id):
    data = request.json

    title = data.get('title', None)
    content = data.get('content', None)
    time = data.get('time', None)
    category = data.get('category_id', None)
    tags = data.get('tags', None)

    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()

    article = session.query(Articles).filter(Articles.id == post_id).first()

    if not article:
        abort(404, 'post not found')

    article.title = title
    article.content = content
    if time:
        article.time = time
    article.category_id = category

    already_exists_tags = [tag.name for tag in article.tags]
    need_remove_tags = list(set(already_exists_tags) - set(tags))
    for tag in tags:
        if tag not in already_exists_tags:
            this_tag_model = session.query(
                Tags).filter(Tags.name == tag).first()
            if not this_tag_model:
                this_tag_model = Tags(tag)
            this_tag_model.articles.append(article)
            session.add(this_tag_model)
    for tag in need_remove_tags:
        this_tag_model = session.query(Tags).filter(Tags.name == tag).first()
        article.tags.remove(this_tag_model)

    session.commit()

    return jsonify({'msg': 'ok'})


@main.route('/post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_article(post_id):
    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()
    article = session.query(Articles).filter(Articles.id == post_id).first()
    
    if not article:
        abort(404, 'article not found')

    session.delete(article)
    session.commit()

    return jsonify({'msg': 'ok'})


# @main.route('/post/')
