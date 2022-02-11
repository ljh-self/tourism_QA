import codecs
import pymysql
import csv

# 打开数据库连接
def get_conn():
    db = pymysql.connect(host="localhost",port=3306,
                   user="root",password="root",
                   db="demo_01",charset="utf8")
    return db
# 在数据库表中插入.csv文件中的数据
def insert(cur, table, args):
    sql = 'insert into ' + table + ' values(%s,%s,%s)'
    try:
        cur.execute(sql, args)
    except Exception as e:
        print(e)
# 查询object的值
def query_object(cur, table, args):
    sql = 'select object from ' + table + ' where subject = %s and predicate = %s'
    try:
        cur.execute(sql, args)
        while 1:
            res = cur.fetchone()
            if res is None:
                # 表示已经取完结果集
                break
            print(res[0])
    except Exception as e:
        print(e)
# 查询subject的值
def query_subject(cur, table, args):
    sql = 'select subject from ' + table + ' where object = %s and predicate = %s'
    try:
        cur.execute(sql, args)
        while 1:
            res = cur.fetchone()
            if res is None:
                # 表示已经取完结果集
                break
            print(res[0])
    except Exception as e:
        print(e)
# 查询predicate的值
def query_predicate(cur, table, args):
    sql = 'select predicate from ' + table + ' where subject = %s and object = %s'
    try:
        cur.execute(sql, args)
        while 1:
            res = cur.fetchone()
            if res is None:
                # 表示已经取完结果集
                break
            print(res[0])
    except Exception as e:
        print(e)
# 读取.csv文件放入mysql中
def read_csv_to_mysql(filename):
    with codecs.open(filename=filename, mode='r+', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = next(reader)
        print(head)
        conn = get_conn()
        cur = conn.cursor()
        # 查询
        list = ['张三','年龄']
        args = tuple(list)
        query_object(cur, 'tb_csv', args)
        # 释放连接
        conn.commit()
        cur.close()
        conn.close()
# 将mysql中的值放入.csv文件中，方便后续批量离线更新知识图谱
def read_mysql_to_csv(filename):
    conn = get_conn()
    cur = conn.cursor()
    sql = 'select * from tb_csv'
    cur.execute(sql.encode('utf-8'))
    data = cur.fetchall()
    with codecs.open(filename=filename, mode='w+', encoding='utf-8') as f:
        write = csv.writer(f)
        for item in data:
            write.writerow(item)
# 主函数
if __name__ == '__main__':
    read_csv_to_mysql(r'C:\\Users\\dell\\Desktop\\data.csv')
    # read_mysql_to_csv('C:\\Users\\dell\\Desktop\\data_new.csv')

