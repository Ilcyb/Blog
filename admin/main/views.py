from . import main
from ..utils.DBHelper import DBHelper
from ..utils.Utils import FetchType, getShortDescFromContent
from flask import render_template

@main.route('/')
def index():
    h = DBHelper()
    sql = 'select A.article_id,A.title,A.time,A.views,C.name from' \
          ' article as A left join category as C on A.category=C.category_id'
    result = [dict(id=article[0], title=article[1], time=article[2].strftime('%Y-%m-%d'), views=article[3], 
                    tag=article[4]) for article in list(h.execute(sql))]
    return render_template('index.html', posts=result)

@main.route('/edit/<int:post_id>')
def post_edit(post_id):
    return render_template('post_edit.html')