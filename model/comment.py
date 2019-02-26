from .common import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Comments(Base):
    __tablename__ = 'Comment'

    id = Column('comment_id', Integer, primary_key=True)
    username = Column('username', String)
    email = Column('email', String)
    time = Column('time', DateTime)
    content = Column('content', String)
    comment_type = Column('type', Integer)
    article_id = Column('article_id', Integer, ForeignKey('Article.article_id'))
    article = relationship('Articles', back_populates='comments')
    respondent_id = Column('respondent_id', Integer)

    def __init__(self, username, email, time, content, article, comment_type, respondent_id):
        self.username = username
        self.email = email
        self.time = time
        self.content = content
        self.article = article
        self.comment_type = comment_type
        self.respondent_id = respondent_id

    def get_map_data(self):
        return {
            'id': self.id,
            'username': self.username or '匿名',
            'email': self.email or '无',
            'time': self.time.strftime('%Y-%m-%d %H:%M'),
            'content': self.content,
            'comment_type': self.comment_type
        }