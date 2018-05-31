from . import blog
from ..utils.DBHelper import DBHelper
from flask import render_template, redirect, url_for


@blog.route('/')
def index(methods=['GET']):
    h = DBHelper()
    sql = 'select A.article_id,A.title,A.content,A.time,A.views,C.name from' \
          ' article as A left join category as C on A.category=C.category_id'
    result = [dict(id=article[0], title=article[1], time=article[3].strftime('%Y-%m-%d'), views=article[4], tag=article[5], desc=article[2])
              for article in list(h.execute(sql))]
    return render_template('index.html', posts=result)

@blog.route('/post/<int:postId>')
def detailPost(postId):
    return redirect(url_for('blog.index'))
