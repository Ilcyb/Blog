from .common import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Articles(Base):
    __tablename__ = 'Article'

    id = Column('article_id', Integer, primary_key=True)
    title = Column('title', String)
    content = Column('content', String)
    time = Column('time', DateTime)
    views = Column('views', Integer)
    category_id = Column('category', Integer, ForeignKey('Category.category_id'))
    category = relationship('Categories', back_populates='articles')
    comments = relationship('Comments', back_populates='article')

    def __init__(self, title, content, time, views, category):
        self.title = title
        self.content = content
        self.time = time
        self.views = views
        self.category = category
