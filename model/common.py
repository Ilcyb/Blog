from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from utils import SingletonMetaclass

Base = declarative_base()

class SessionFactory(metaclass=SingletonMetaclass):

    def __init__(self, user, password, host, port, database):
        self._conn_string = self._get_conn_string(user, password, host, port, database)
        self._engine = create_engine(self._conn_string)
        self._sessionmaker = self._get_sessionmaker(self._engine)

    def _get_conn_string(self, user, password, host, port, database):
        pass

    def _get_sessionmaker(self, engine):
        return sessionmaker(bind=engine)

    def get_session(self) -> Session:
        return self._sessionmaker()

# @singleton
class PyMySqlSessionFactory(SessionFactory):

    def _get_conn_string(self, user, password, host, port, database):
        return 'mysql+pymysql://%s:%s@%s:%d/%s' % (user, password, host, port, database)
