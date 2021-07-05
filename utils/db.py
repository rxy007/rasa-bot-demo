import pymysql
from utils.db_config import *


class DB:
    def __init__(self):
        self.connect = self.create_connect()

    def create_connect(self):
        try:
            connect = pymysql.connect(host=host, database=database, user=user_name, password=password, port=port)
        except Exception as e:
            print('数据库连接失败')
            print(e)
            connect = None
        return connect

    def close(self):
        if self.connect:
            self.connect.close()

    def insert(self, table_name, data: dict):
        if not self.connect:
            self.connect = self.create_connect()
        if self.connect:
            sql = "insert into " + table_name
            key, value = "(", "values ("
            for k, v in data.items():
                key += k + ", "
                if isinstance(v, int) or isinstance(v, float):
                    value += str(v) + ", "
                else:
                    value += "'" + v + "', "
            key = key[:-2] + " ) "
            value = value[:-2] + " )"
            sql += key + value
            cursor = self.connect.cursor()
            try:
                cursor.execute(sql)
                self.connect.commit()
            except Exception as e:
                print(e)
                self.connect.rollback()
            finally:
                cursor.close()


db = DB()

if __name__ == '__main__':
    import datetime
    table_name = 'user_info'
    data = {
        'has_che': 0,
        'has_fang': 0,
        'has_xin': 0,
        'has_wei': 0,
        'has_zhi': 1,
        'phone_number': '19908080808',
        'create_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'update_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    db.insert(table_name, data)