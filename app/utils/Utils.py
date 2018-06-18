from enum import Enum

def assembleQuerySqlString(tableName, keywords, conjunction, *args):
    sql1 = 'select ' + ','.join(args) + ' from ' + tableName
    sql2 = ' where '
    flag = 1
    sql3 = ''
    for key, value in keywords.items():
        if flag == 1:
            sql3 += (' {}={} '.format(key, str(value)))
            flag += 1
        else:
            sql3 += ('{} {}={} '.format(conjunction or '', key, str(value)))
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
        tempList.append("{}={}".format(key, str(value)))
    sql2 = ','.join(tempList)

    tempList = list()
    for key, value in conditions.items():
        tempList.append("{}={}".format(key, str(value)))
    sql3 += (conjunction or '' + ' ').join(tempList)

    return sql1 + sql2 + sql3
    
def assembleDeleteSqlString(tableName, condition, conjunction):
    sql1 = 'delete from ' + tableName + ' where '
    sql2 = ''

    tempList = list()
    for key, value in condition.items():
        tempList.append(str(key) + "='" + str(value) + "'")
    sql2 = (conjunction or '' + ' ').join(tempList)

    return sql1+ sql2

def getShortDescFromContent(content, threshold=100):
    if len(content) < threshold:
        return content
    # count = 0
    # for i in range(threshold):
    #     if content[count].isspace():
    #         break
    #     count += 1
    # return content[:count]
    return content[:threshold] + "..."

class FetchType(Enum):
    FetchOne = 0
    FetchMany = 1