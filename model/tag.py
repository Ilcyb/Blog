from .common import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

tag_article_table = Table(
    'tag_article',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('Tag.tag_id')),
    Column('article_id', Integer, ForeignKey('Article.article_id'))
)

class Tags(Base):
    __tablename__ = 'Tag'

    id = Column('tag_id', Integer, primary_key=True)
    name = Column('name', String)
    articles = relationship('Articles', secondary=tag_article_table)

    def __init__(self, name):
        self.name = name

    def get_map_data(self):
        return {
            'id': self.id,
            'name': self.name
        }
