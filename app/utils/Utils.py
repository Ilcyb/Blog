from enum import Enum

def assembleQuerySqlString(tableName, keywords, conjunction, *args):
    sql1 = 'select ' + ','.join(args) + ' from ' + tableName
    sql2 = ' where '
    flag = 1
    sql3 = ''
    for key, value in keywords.items():
        if flag == 1:
            sql3 += (key + '=\'' + value + '\' ')
            flag += 1
        else:
            sql3 += (conjunction + ' ' + key + '=\'' + value + '\' ')
    return sql1 + sql2 + sql3

def assembleInsertSqlString(tableName, keywords, values):
    sql = 'insert into ' + tableName + ' (' + ','.join(keywords) + ') values(\'' + '\',\''.join(values) + '\')';
    return sql

def assembleUpdateSqlString(tableName, newValues, conditions, conjunction):
    sql1 = 'update ' + tableName + ' set '
    sql2 = ''
    sql3 = ' where '
    tempList = list()
    for key, value in newValues.items():
        tempList.append(key + "='" + value + "'")
    sql2 = ','.join(tempList)

    tempList = list()
    for key, value in conditions.items():
        tempList.append(key + "='" + value + "'")
    sql3 += (conjunction + ' ').join(tempList)

    return sql1 + sql2 + sql3
    
def assembleDeleteSqlString(tableName, condition, conjunction):
    sql1 = 'delete from ' + tableName + ' where '
    sql2 = ''

    tempList = list()
    for key, value in condition.items():
        tempList.append(key + "='" + value + "'")
    sql2 = (conjunction + ' ').join(tempList)

    return sql1+ sql2


class FetchType(Enum):
    FetchOne = 0
    FetchMany = 1