import os
import datetime
import csv
from Core.Log import Log
from Util.MongoHelper import MongoHelper
from Util.MySqlHelper import MysqlHelper
from Util.CSVHelper import *


class DaoBase(object):
    mongo_client = None
    mysql_conn = None
    mysql_cursor = None
    rows = []

    def __init__(self, **kwargs):
        self._run_date = kwargs.get("run_date", datetime.datetime.now())
        self.log = kwargs.get('log', Log(self.__class__.__name__))
        self.kwargs = kwargs

    def connect_to_mongo(self):
        self.mongo_client = MongoHelper().connect(**self.kwargs)

    def connect_to_mysql(self):
        mysql = MysqlHelper(**self.kwargs)
        mysql.connect()
        self.mysql_conn = mysql.conn
        self.mysql_cursor = mysql.cursor

    def save(self, source_block):
        self.rows.append(source_block)
        pass

    def parse_data(self, source_block):
        pass

    def parse(self, **kwargs):
        pass

    def df_to_mysql(self, df, table, if_exists):
        mysql_config = {
            "charset": os.getenv('MYSQL_CHARSET', 'utf8mb4'),
            "db": os.getenv('MYSQL_DB', 'test'),
            "host": os.getenv('MYSQL_HOST', '127.0.0.1'),
            "port": os.getenv('MYSQL_PORT', 3306),
            "user": os.getenv('MYSQL_USER', 'dev'),
            "password": os.getenv('MYSQL_PASSWORD', 'Devadmin001')
        }
        from sqlalchemy import create_engine
        engine = create_engine('mysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'.format(**mysql_config))
        with engine.connect() as conn, conn.begin():
            df.to_sql(table, conn, if_exists=if_exists, index=False)

    def csv_to_mysql(self, file, table=None, if_exists='append'):
        import pandas as pd
        if table is None:
            import re
            table = re.search('(\D+)', file.split('/')[-1]).group(1).strip('_')
        df = pd.read_csv(file)
        self.df_to_mysql(df, table, if_exists)
        self.log.info('load csv file to mysql successfuly')

    def export_data_to_csv(self, file, rows=None, fields=None):
        '''

        :param file: file name to export .csv
        :param rows: data rows
        :param fields: columns of csv
        :return:
        '''
        if not rows:
            rows = self.rows
        if not fields:
            fields = rows[0].keys()
        export_rows_to_csv(file, rows, fields)

    def select(self, sql):
        if not self.mysql_cursor:
            self.connect_to_mysql()
        self.mysql_cursor.execute(sql)
        result = self.mysql_cursor.fetchall()
        self.mysql_conn.close()
        return result
