from .ConnPool import MyConnPool
from .Utils import *


class DBHelper(object):

    def __init__(self):
        self.conn = MyConnPool.getPool().connection()

    def __del__(self):
        self.conn.close()

    def execute(self, sql):
        try:
            self.conn.begin()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        
    def executeQuery(self, fetchType, tableName, keywords, conjunction, *args):
        try:
            cursor = self.conn.cursor()
            cursor.execute(assembleQuerySqlString(tableName, keywords, conjunction, *args))
            if(fetchType == FetchType.FetchOne):
                r = cursor.fetchone()
                return r
            elif(fetchType == FetchType.FetchMany):
                r = cursor.fetchmany()
                return r
            else:
                raise ValueError('illegal fetchType argument')
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def executeInsert(self, tableName, keywords, values):
        try:
            self.conn.begin()
            cursor = self.conn.cursor()
            flag = cursor.execute(assembleInsertSqlString(tableName, keywords, values))
            self.conn.commit()
            return flag
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def executeUpdate(self, tableName, newValues, conditions, conjunction):
        try:
            self.conn.begin()
            cursor = self.conn.cursor()
            flag = cursor.execute(assembleUpdateSqlString(tableName, newValues, conditions, conjunction))
            self.conn.commit()
            return flag
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        
    def executeDelete(self, tableName, condition, conjunction):
        try:
            self.conn.begin()
            cursor = self.conn.cursor()
            flag = cursor.execute(assembleDeleteSqlString(tableName, condition, conjunction))
            self.conn.commit()
            return flag
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()