from . import main
from ..utils.DBHelper import DBHelper
from ..utils.Utils import FetchType, getShortDescFromContent
from ..utils.Decorators import login_required
from flask import render_template, request, session, redirect, url_for, abort
from time import time

@main.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        h = DBHelper()
        sql = 'select count(1) from admin where username=%s and password=%s'
        result = h.execute(sql, (username, password))
        if result[0][0] == 1:
            session['is_admin'] = True
            session['username'] = username
    except Exception as e:
        print(e)
        return redirect(url_for('main.login_page'))
    else:
        return redirect(url_for('main.index'))

@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.login_page'))

@main.route('/')
@login_required
def index():
    h = DBHelper()
    sql = 'select A.article_id,A.title,A.time,A.views,C.name from' \
          ' Article as A left join Category as C on A.category=C.category_id'
    result = [dict(id=article[0], title=article[1], time=article[2].strftime('%Y-%m-%d'), views=article[3], 
                    tag=article[4]) for article in list(h.execute(sql))]
    return render_template('index.html', posts=result, username=session['username'])

@main.route('/post', methods=['GET'])
@login_required
def create_post_page():
    h = DBHelper()
    sql = 'select category_id, name from Category'
    result = h.execute(sql)
    categories = [dict(id=category[0],name=category[1]) for category in result]
    return render_template('post.html', username=session['username'], categories=categories)

@main.route('/post', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    tags = request.form['tags']
    post_time = request.form.get('time', None) or time()
    try:
        h = DBHelper()
        sql = 'insert into Article(title,content,category) values(%s,%s,%s)'
        article_id = h.executeRawInsert(sql, (title, content, int(category)))
        tag_id_list = insert_tag(tags)
        insert_article_tag(tag_id_list, article_id)
    except Exception as e:
        print(e)
        return redirect(url_for('main.create_post'))
    else:
        return redirect(url_for('main.index'))

@main.route('/edit/<int:post_id>', methods=['GET'])
@login_required
def get_edit_post_page(post_id):
    h = DBHelper()
    sql = 'select title,content,category from Article where article_id = %s'
    result = h.execute(sql, (post_id))[0]
    if len(result) == 0:
        abort(404)
    tags = '|'.join(get_tags(post_id))
    categories_sql = 'select category_id, name from Category'
    categories_result = h.execute(categories_sql)
    categories = [dict(id=category[0], name=category[1]) for category in categories_result]
    post = dict(id=post_id, title=result[0], content=result[1], category=result[2], tags=tags)
    return render_template('post_edit.html', username=session['username'], post=post, categories=categories)

@main.route('/edit/<int:post_id>', methods=['POST'])
@login_required
def update_post(post_id):
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    tags = request.form['tags']
    post_time = request.form.get('time', None) or time()
    try:
        h = DBHelper()
        sql = 'update Article set title = %s,content = %s,category = %s where article_id=%s'
        h.execute(sql, (title, content, int(category), post_id))
        insert_tag(tags)
        tags = tags.split('|')
        removed_tags, new_ids = get_removed_tags_ids(tags, post_id)
        if len(removed_tags) > 0:
            delete_tag_list(removed_tags, post_id)
        insert_article_tag(new_ids, post_id)
    except Exception as e:
        print(e)
        return redirect(url_for('main.get_edit_post_page', post_id=post_id))
    else:
        return redirect(url_for('main.index'))

def insert_tag(tags:str):
    tag_list = tags.split('|')
    h = DBHelper()
    sql = "select tag_id, name from Tag where name in ('%s')" % "','".join(tag_list)
    result = [dict(id=tag[0], name=tag[1]) for tag in list(h.execute(sql))]
    already_exists_tags = [d['name'] for d in result]
    for tag in tag_list:
        if tag not in already_exists_tags:
            temp_id = h.executeRawInsert("insert into Tag(name) values(%s)", (tag))
            result.append(dict(id=temp_id, name=tag))
    return [i['id'] for i in result]

def insert_tag_list(tags):
    h = DBHelper()
    sql = "select tag_id, name from Tag where name in ('%s')" % "','".join(tags)
    result = [dict(id=tag[0], name=tag[1]) for tag in list(h.execute(sql))]
    already_exists_tags = [d['name'] for d in result]
    for tag in tags:
        if tag not in already_exists_tags:
            temp_id = h.executeRawInsert("insert into Tag(name) values(%s)", (tag))
            result.append(dict(id=temp_id, name=tag))
    return [i['id'] for i in result]

def get_removed_tags_ids(tags, post_id):
    h = DBHelper()
    sql = 'select tag_id from tag_article where article_id = %s'
    origin_tag_ids = [tag[0] for tag in list(h.execute(sql, post_id))]
    sql = "select tag_id from Tag where name in ('%s')" % "','".join(tags)
    now_tag_ids = [tag[0] for tag in list(h.execute(sql))]
    removed_ids = []
    new_ids = []
    for tag_id in origin_tag_ids:
        if tag_id not in now_tag_ids:
            removed_ids.append(tag_id)
    for tag_id in now_tag_ids:
        if tag_id not in origin_tag_ids:
            new_ids.append(tag_id)
    return removed_ids, new_ids

def delete_tag_list(tags_ids, post_id):
    h = DBHelper()
    tags_ids = [str(tag_id) for tag_id in tags_ids]
    sql = "delete from tag_article where tag_id in (%s) and article_id = %d" % (','.join(tags_ids), post_id)
    h.execute(sql)

def insert_article_tag(tags:list, article_id:int):
    h = DBHelper()
    for i in range(len(tags)):
        h.execute("insert into tag_article values(%d, %d)" % (tags[i], article_id))

def get_tags(post_id:int):
    h = DBHelper()
    sql = 'select T.name from Tag as T left join tag_article as TA on T.tag_id = TA.tag_id where TA.article_id = %s'
    result = h.execute(sql, (post_id))
    tags = [tag[0] for tag in result]
    return tags