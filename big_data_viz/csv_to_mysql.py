# encoding: utf-8
# @time :  2022-06-07 21:03:00
# @file : csv_to_mysql.py
# @software : PyCharm
# @author : Ading
# Official Account: AdingBLOG
import csv

import pymysql

DB_CONFIG = {
    '00': {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "dataviz2022"
    }
}
class MysqlUtil:
    """
    utility class, for mysql connection and record manipulation
    """

    db = None
    cur = None

    def __init__(self, db_config):
        '''
        构造方法, 初始化db 和cur
        '''
        self.db = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            charset='utf8mb4',
            read_timeout=30,
            write_timeout=30
        )
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def insert(self, table, keys, values):
        """
        sql statements, insert
        :param table:
        :param keys:
        :param values:
        :return:
        """
        values_num = []
        for i in values:
            values_num.append(r'%s')
        sql = "insert into {} ({}) values ({})".format(table, ','.join(keys), ','.join(values_num))
        print(sql)
        self.cur.execute(sql, values)
        self.db.commit()

class CSV2Mysql:
    def __init__(self, csvFilename):
        self.csv_file = open(csvFilename,'r',encoding="utf-8")
        self.csv_reader = csv.reader(self.csv_file)

    def insert_sql(self,table, conn:MysqlUtil,table_fields:list):
        flag = True
        for row in self.csv_reader:
            if flag:
                flag = False
                continue
            conn.insert(table=table,keys=table_fields,values=row)
            print("{} inserted".format(row[0]))

if __name__ == '__main__':
    conn = MysqlUtil(DB_CONFIG['00'])
    csv2mysql = CSV2Mysql("./data/cleansed/fifa-2019-cleansed.csv")
    table_fields = ["name","age","potential","body_type","value","wage"]
    csv2mysql.insert_sql("fifa_player_2019",conn,table_fields)