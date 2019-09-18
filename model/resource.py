from .common import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
import datetime


class Resources(Base):
    __tablename__ = 'Resource'

    id = Column('resource_id', Integer, primary_key=True)
    user_type = Column('user_type', Integer)
    file_name = Column('file_name', String)
    file_type = Column('file_type', Integer)
    url = Column('url', String)
    time = Column('time', DateTime, default=datetime.datetime.now)

    def __init__(self, user_type, file_name, file_type, url, time=None):
        self.user_type = user_type
        self.file_name = file_name
        self.file_type = file_type
        self.url = url
        self.time = time

    def __repr__(self):
        return '[%d]:%s(%s)' % (self.id, self.file_name, self.url)

    def get_map_data(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'url': self.url
        }
