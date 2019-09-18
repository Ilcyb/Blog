from .common import Base
from sqlalchemy import Column, Integer, Text

class About(Base):
    __tablename__ = 'About'

    id = Column('about_id', Integer, primary_key=True)
    type = Column('type', Integer)
    parse_type = Column('parse_type', Integer)
    describetion = Column('describetion', Text)

    def __init__(self, type, parse_type, content):
        self.type = type
        self.parse_type = parse_type
        self.content = content

    def get_map_data(self):
        data = {
            'describetion': self.describetion
        }
        if self.parse_type == 0:
            data['parse_type'] = 'markdown'
        elif self.parse_type == 1:
            data['parse_type'] = 'html'
        else:
            raise ValueError('value of parse_type is invalid')

        return data
