from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from utils import SingletonMetaclass
from flask import current_app

Base = declarative_base()


class SessionFactory(metaclass=SingletonMetaclass):

    def __init__(self, user, password, host, port, database):
        self._conn_string = self._get_conn_string(
            user, password, host, port, database)
        self._engine = create_engine(self._conn_string)
        self._sessionmaker = self._get_sessionmaker(self._engine)

    def _get_conn_string(self, user, password, host, port, database):
        pass

    def _get_sessionmaker(self, engine):
        return sessionmaker(bind=engine)

    def get_session(self) -> Session:
        return self._sessionmaker()


class PyMySqlSessionFactory(SessionFactory):

    def _get_conn_string(self, user, password, host, port, database):
        return 'mysql+pymysql://%s:%s@%s:%d/%s' % (user, password, host, port, database)


def getSessionFactory() -> SessionFactory:
    sessionFactory = PyMySqlSessionFactory(
        current_app.config['MYSQL_USERNAME'],
        current_app.config['MYSQL_PASSWORD'],
        current_app.config['MYSQL_HOST'],
        int(current_app.config['MYSQL_PORT']),
        current_app.config['BLOG_DATABASE']
    )

    return sessionFactory
