import pymysql
from DBUtils.PooledDB import PooledDB
from flask import current_app

class MyConnPool:

    pool = None

    @classmethod
    def getPool(cls):
        if cls.pool == None:
            cls.pool = PooledDB(pymysql, maxcached=10, maxconnections=10, 
                                host=current_app.config['MYSQL_HOST'],
                                user=current_app.config['MYSQL_USERNAME'],
                                passwd=current_app.config['MYSQL_PASSWORD'],
                                db=current_app.config['MYSQL_DB'],
                                port=3306,
                                charset=current_app.config['MYSQL_CHARSET'])
        return cls.pool
