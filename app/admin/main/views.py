from . import admin
from model import getSessionFactory, Articles, Categories, Tags, Admin, Resources
from utils import enctry_string, dectry_string, get_page, allowed_file, upload_file_to_qiniu, get_file_extension, get_file_type
from flask import render_template, request, session as flask_session, redirect, url_for, abort, current_app
from time import time
from functools import wraps
import datetime

def login_required(func):
    @wraps(func)
    def handle_args(*args, **kwargs):
        user_id = flask_session.get('user_id', None)
        username = flask_session.get('username', None)

        if not user_id or not username:
            return redirect(url_for('admin.login_page'))

        sessionFactory = getSessionFactory()
        query_session = sessionFactory.get_session()
        user = query_session.query(Admin).filter(
            Admin.id == int(user_id), Admin.username == username).first()
        query_session.close()

        if user is None:
            return redirect(url_for('admin.login_page'))

        return func(*args, **kwargs)
    return handle_args

@admin.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@admin.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        if not username or not password:
            abort(400, 'bad request')

        sessionFactory = getSessionFactory()
        session = sessionFactory.get_session()
        user = session.query(Admin).filter(
            Admin.username == username, Admin.password == password).first()
        session.close()

        if user is None:
            abort(401, 'wrong password')

        flask_session['user_id'] = user.id
        flask_session['username'] = user.username
    except Exception as e:
        print(e)
        return redirect(url_for('admin.login_page'))
    else:
        return redirect(url_for('admin.index'))

@admin.route('/logout', methods=['GET'])
def logout():
    flask_session.clear()
    return redirect(url_for('admin.login_page'))

@admin.route('/')
@login_required
def index():
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)
    session = getSessionFactory().get_session()
    articles = session.query(Articles).order_by(
        Articles.id).offset(offset).limit(limit).all()
    article_datas = [article.get_map_data() for article in articles]
    categories = session.query(Categories).order_by(Categories.id).all()
    category_datas = [category.get_map_data() for category in categories]
    session.close()

    return render_template('index.html', posts=article_datas, 
    username=flask_session['username'], categories=category_datas)

@admin.route('/post', methods=['GET'])
@login_required
def create_post_page():
    session = getSessionFactory().get_session()
    categories = session.query(Categories).order_by(Categories.id).all()
    category_datas = [category.get_map_data() for category in categories]
    session.close()

    return render_template('post.html', username=flask_session['username'], categories=category_datas)

@admin.route('/post', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    tags = request.form['tags']
    if request.form.get('time', None):
        post_time = datetime.datetime.fromtimestamp(request.form.get('time'))
    else:
        post_time = datetime.datetime.now()
    try:
        if not title or not content or not category:
            abort(400, 'invalid request')
        session = getSessionFactory().get_session()
        new_article = Articles(title, content, post_time, 0, int(category))
        session.add(new_article)

        tags = tags.split('|')
        for tag in tags:
            this_tag = session.query(Tags).filter(Tags.name == tag).first()
            if not this_tag:
                this_tag = Tags(tag)
            this_tag.articles.append(new_article)
            session.add(this_tag)

        session.commit()
        session.close()
    except Exception as e:
        print(e)
        return redirect(url_for('admin.create_post'))
    else:
        return redirect(url_for('admin.index'))

@admin.route('/edit/<int:post_id>', methods=['GET'])
@login_required
def get_edit_post_page(post_id):
    session = getSessionFactory().get_session()
    article = session.query(Articles).filter(Articles.id == post_id).first()
    categories = session.query(Categories).order_by(Categories.id).all()
    if not article:
        abort(404)

    article = article.get_map_data()
    tags = '|'.join([tag['name'] for tag in article['tags']])
    category = article['category']
    article['category'] = category['name']
    article['tags'] = tags
    categories = [category.get_map_data() for category in categories]
    session.close()
    return render_template('post_edit.html', username=flask_session['username'], post=article, categories=categories)

@admin.route('/edit/<int:post_id>', methods=['POST'])
@login_required
def update_post(post_id):
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    tags = request.form['tags'].split('|')

    try:
        sessionFactory = getSessionFactory()
        session = sessionFactory.get_session()

        article = session.query(Articles).filter(Articles.id == post_id).first()

        if not article:
            abort(404, 'post not found')

        article.title = title
        article.content = content
        article.category_id = category
        article.tags = []

        for tag in tags:
            this_tag = session.query(Tags).filter(Tags.name == tag).first()
            if not this_tag:
                this_tag = Tags(tag)
            this_tag.articles.append(article)
            session.add(this_tag)
        # already_exists_tags = [tag.name for tag in article.tags]
        # need_remove_tags = list(set(already_exists_tags) - set(tags))
        # for tag in tags:
        #     if tag not in already_exists_tags:
        #         this_tag_model = session.query(
        #             Tags).filter(Tags.name == tag).first()
        #         if not this_tag_model:
        #             this_tag_model = Tags(tag)
        #         this_tag_model.articles.append(article)
        #         session.add(this_tag_model)
        # for tag in need_remove_tags:
        #     this_tag_model = session.query(Tags).filter(Tags.name == tag).first()
        #     article.tags.remove(this_tag_model)

        session.commit()
        session.close()
    except Exception as e:
        print(e)
        # return redirect(url_for('admin.get_edit_post_page', post_id=post_id))
        raise e
    else:
        return redirect(url_for('admin.index'))

@admin.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete_post(post_id):
    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()
    article = session.query(Articles).filter(Articles.id == post_id).first()

    if not article:
        abort(404, 'article not found')

    session.delete(article)
    session.commit()
    session.close()
    return redirect(url_for('admin.index'))

# @admin.route('/search', methods=['POST'])
# @login_required
# def search_posts():
#     title = request.form['title']
#     category = int(request.form['category'])
#     h = DBHelper()
#     sql = "select A.article_id,A.title,A.time,A.views,C.name from" \
#           " Article as A left join Category as C on A.category=C.category_id where "
#     if title:
#         sql += "A.title like '%{}%' or A.category = {}"
#         sql = sql.format(title, category)
#         result = [dict(id=article[0], title=article[1], time=article[2].strftime('%Y-%m-%d'), views=article[3],
#                        tag=article[4]) for article in list(h.execute(sql))]
#     else:
#         sql += "A.category = %d"
#         sql = sql % category
#         result = [dict(id=article[0], title=article[1], time=article[2].strftime('%Y-%m-%d'), views=article[3],
#                        tag=article[4]) for article in list(h.execute(sql))]
#     categories_sql = 'select category_id, name from Category'
#     categories_result = h.execute(categories_sql)
#     categories = [dict(id=category[0],name=category[1]) for category in categories_result]
#     return render_template('index.html', posts=result, username=flask_session['username'], categories=categories)

@admin.route('/resource', methods=['GET'])
@login_required
def resource_manage():
    query_data = request.args

    page = int(query_data.get('page', 1))
    size = int(query_data.get('size', current_app.config['ARTICLE_PER_PAGE']))

    if page <= 0 or size <= 0:
        abort(400)

    offset, limit = get_page(page, size)
    session = getSessionFactory().get_session()
    resources = session.query(Resources) \
                .order_by(Resources.id.desc()).offset(offset).limit(limit).all()
    resources_data = [resource.get_map_data() for resource in resources]
    return render_template('resourceUpload.html', resources = resources_data)

@admin.route('/resource', methods=['POST'])
@login_required
def upload_resource():
    if 'file' not in request.files:
        abort(400, 'no file has been uploaded.')
    file = request.files['file']
    if file.filename == '':
        abort(400, 'no file has been uploaded')

    file_extension = get_file_extension(file.filename)
    if file and allowed_file(file_extension, current_app.config['ALLOWED_EXTENSIONS']):
        ret = upload_file_to_qiniu(current_app.config['QINIU_ACCESS_KEY'],
                             current_app.config['QINIU_SECRET_KEY'], 
                             current_app.config['QINIU_BUCKET_NAME'], 
                             file.filename, file.read())
        if not ret['ret']:
            abort(500, ret['msg'])
    else:
        abort(400, 'not allowed file type.')
    
    url = f"http://{current_app.config['QINIU_BUCKET_URL']}/{ret['key']}"
    file_type = get_file_type(file_extension)
    
    sessionFactory = getSessionFactory()
    session = sessionFactory.get_session()

    new_resource = Resources(0, file.filename, file_type, url)
    session.add(new_resource)
    session.commit()
    session.close()

    return redirect(url_for('admin.resource_manage'))
