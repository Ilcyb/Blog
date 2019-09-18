from .common import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

class Categories(Base):
    __tablename__ = 'Category'

    id = Column('category_id', Integer, primary_key=True)
    name = Column('name', String)
    articles = relationship('Articles', back_populates='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '[%d]:%s' % (self.id, self.name)

    def get_map_data(self):
        return {
            'id': self.id,
            'name': self.name
        }
