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
    article_id = Column('article_id', Integer, ForeignKey('Article.article_id'))
    article = relationship('Articles', back_populates='comments')

    def __init__(self, username, email, time, content, article):
        self.username = username
        self.email = email
        self.time = time
        self.content = content
        self.article = article