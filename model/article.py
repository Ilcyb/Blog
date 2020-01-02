from .common import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .tag import tag_article_table
import datetime

class Articles(Base):
    __tablename__ = 'Article'

    id = Column('article_id', Integer, primary_key=True)
    title = Column('title', String)
    content = Column('content', String)
    time = Column('time', DateTime, default=datetime.datetime.now)
    views = Column('views', Integer)
    category_id = Column('category', Integer, ForeignKey('Category.category_id'))
    category = relationship('Categories', back_populates='articles')
    comments = relationship('Comments', back_populates='article')
    tags = relationship('Tags', secondary=tag_article_table)

    def __init__(self, title, content, time, views, category_id):
        self.title = title
        self.content = content
        self.time = time
        self.views = views
        self.category_id = category_id

    def get_map_data(self):
        data = {
            'id': self.id,
            'title': self.title,
            'time': self.time.strftime('%Y-%m-%d %H:%M'),
            'content': self.content,
            'views': self.views,
            'category': self.category.get_map_data()
        }

        comments = []

        for comment in self.comments:
            comments.append(comment.get_map_data())

        tags = []
        for tag in self.tags:
            tags.append(tag.get_map_data())

        data['comments'] = comments
        data['tags'] = tags

        return data
