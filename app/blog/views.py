from . import blog
from ..utils.DBHelper import DBHelper
from ..utils.Utils import FetchType, getShortDescFromContent
from flask import render_template, redirect, url_for, abort


@blog.route('/')
def index(methods=['GET']):
    h = DBHelper()
    sql = 'select A.article_id,A.title,A.content,A.time,A.views,C.name from' \
          ' article as A left join category as C on A.category=C.category_id'
    result = [dict(id=article[0], title=article[1], time=article[3].strftime('%Y-%m-%d'), views=article[4], 
                    tag=article[5], desc=getShortDescFromContent(article[2]))
              for article in list(h.execute(sql))]
    return render_template('index.html', posts=result)

@blog.route('/post/<int:postId>')
def detailPost(postId):
    h = DBHelper()
    sql = 'select A.title,A.content,A.time,A.views,C.name from' \
          ' article as A left join category as C on A.category=C.category_id where A.article_id = ' + str(postId)
    result = h.execute(sql)
    if len(result) == 0:
        abort(404)
    else:
        article = result[0]
        post = dict(id=postId, title=article[0], time=article[2].strftime('%Y-%m-%d'), views=article[3], tag=article[4], content=article[1])
        h.executeUpdate('article', dict(views=article[3]+1), dict(article_id=postId), None)
        # h.execute("update article set views={} where article_id={}".format(str(article[3]+1), str(postId)))
        print(article[3]+1)
        return render_template('post.html', post=post)
