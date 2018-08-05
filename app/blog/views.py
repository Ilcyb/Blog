from . import blog
from ..utils.DBHelper import DBHelper
from ..utils.Utils import FetchType, getShortDescFromContent
from flask import render_template, redirect, url_for, abort, current_app


@blog.route('/')
def index(methods=['GET']):
    h = DBHelper()
    sql = 'select A.article_id,A.title,A.content,A.time,A.views,C.name from' \
          ' Article as A left join Category as C on A.category=C.category_id'
    result = [dict(id=article[0], title=article[1], time=article[3].strftime('%Y-%m-%d'), views=article[4], 
                    category=article[5], desc=getShortDescFromContent(article[2]))
              for article in list(h.execute(sql))]
    return render_template('index.html', posts=result)

@blog.route('/post/<int:postId>')
def detailPost(postId):
    h = DBHelper()
    sql = 'select A.title,A.content,A.time,A.views,C.name from' \
          ' Article as A left join Category as C on A.category=C.category_id where A.article_id = ' + str(postId)
    result = h.execute(sql)
    if len(result) == 0:
        abort(404)
    else:
        article = result[0]
        h.executeUpdate('Article', dict(views=article[3]+1), dict(article_id=postId), None)
        post = dict(id=postId, title=article[0], time=article[2].strftime('%Y-%m-%d'), views=article[3]+1, category=article[4], content=article[1])

        sql = 'select article_id,title from Article order by views desc limit ' + str(current_app.config['HOTEST_ARTICLE_NUMS'])
        hotest_articles = h.execute(sql)
        hotest_posts = [dict(id=article_tuple[0], title=article_tuple[1]) for article_tuple in hotest_articles]
        return render_template('post.html', post=post, hotest_posts=hotest_posts)
