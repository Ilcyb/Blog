from .common import Base
from sqlalchemy import Column, Integer, String

class Admin(Base):
    __tablename__ = 'admin'

    id = Column('admin_id', Integer, primary_key=True)
    username = Column('username', String)
    password = Column('password', String)

    def __init__(self, username, password):
        self.username = username
        self.password = password