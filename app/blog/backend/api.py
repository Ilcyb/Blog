from . import blog
from model import getSessionFactory, Articles, Categories, Comments, About, Tags
from flask import render_template, redirect, url_for, abort, current_app, request, abort, jsonify
from utils import get_page
from sqlalchemy.orm.session import Session
import datetime


@blog.route('/posts', methods=['GET'])
def get_articles():
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)

    session = getSessionFactory().get_session()
    try:
        articles = session.query(Articles).order_by(
            Articles.id.desc()).offset(offset).limit(limit).all()
        datas = []
        for article in articles:
            datas.append(article.get_map_data())
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify({'datas': datas, 'pager': {'page': page, 'size': size}})


@blog.route('/post/<int:post_id>', methods=['GET'])
def get_article(post_id):
    try:
        session = getSessionFactory().get_session()
        article = session.query(Articles).filter(Articles.id == post_id).first()
        if not article:
            session.close()
            abort(404)

        data = article.get_map_data()
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify(data)


@blog.route('/categories', methods=['GET'])
def get_categories():
    try:
        session = getSessionFactory().get_session()
        categories = session.query(Categories).order_by(Categories.id).all()
        session.close()

        datas = []
        for category in categories:
            datas.append(category.get_map_data())
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify({'datas': datas})


@blog.route('/category/<int:category_id>/posts', methods=['GET'])
def get_articles_by_category(category_id):
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)

    try:
        session = getSessionFactory().get_session()
        articles = session.query(Articles).filter(Articles.category_id == category_id).order_by(
            Articles.id).offset(offset).limit(limit).all()

        datas = []
        for article in articles:
            datas.append(article.get_map_data())
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

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
    
    try:
        session_factory = getSessionFactory()
        session = session_factory.get_session()
        new_comment = Comments(username, email, None, content, post_id, comment_type, None)
        session.add(new_comment)
        session.commit()
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
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
    
    try:
        session_factory = getSessionFactory()
        session = session_factory.get_session()
        new_comment = Comments(username, email, None, content, post_id, comment_type, comment_id)
        session.add(new_comment)
        session.commit()
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify({'ret': True})


@blog.route('/about/simple', methods=['GET'])
def get_simple_about_me():
    try:
        session_factory = getSessionFactory()
        session = session_factory.get_session()
        about = session.query(About).filter(About.type == 0).first()
        if not about:
            return jsonify({})
        data = about.get_map_data()
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify(data)


@blog.route('/footer', methods=['GET'])
def get_footer_info():
    data = {
        'name': current_app.config['MY_NAME'],
        'email': current_app.config['MY_EMAIL'],
        'power': current_app.config['POWER'],
        'power_url': current_app.config['POWER_URL'],
        'beian': current_app.config['BEIAN'],
        'beian_url': current_app.config['BEIAN_URL'],
        'current_year': datetime.datetime.now().year
    }

    return jsonify(data)


@blog.route('/tags', methods=['GET'])
def get_tags():
    try:
        session_factory = getSessionFactory()
        session = session_factory.get_session()
        sql = '''
        select Tag.tag_id, Tag.name, count(1) as count from tag_article as ta 
        left join Tag on ta.tag_id = Tag.tag_id 
        group by(tag_id) order by count desc, Tag.tag_id
        '''
        tags = session.execute(sql)
        datas = []
        for tag in tags:
            datas.append(dict(id=tag[0], name=tag[1]))
    except Exception as e:
        abort(500, 'something is wrong')
    finally:
        session.close()

    return jsonify({'datas': datas})
