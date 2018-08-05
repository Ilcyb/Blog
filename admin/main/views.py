from . import main
from ..utils.DBHelper import DBHelper
from ..utils.Utils import FetchType, getShortDescFromContent
from ..utils.Decorators import login_required
from flask import render_template, request, session, redirect, url_for
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

@main.route('/edit/<int:post_id>')
@login_required
def post_edit(post_id):
    return render_template('post_edit.html', username=session['username'])

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

def insert_article_tag(tags:list, article_id:int):
    h = DBHelper()
    for i in range(len(tags)):
        h.execute("insert into tag_article values(%d, %d)" % (tags[i], article_id))