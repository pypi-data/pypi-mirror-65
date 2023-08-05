import csv
import datetime
import os
import inspect
from Util.JobHelper import debug


class MysqlHelper:
    conn = None
    cursor = None

    def __init__(self, **kwargs):
        self.mysql_hook = kwargs.get('mysql_hook')
        self.kwargs = kwargs

    def use_pymysql_connect(self):
        import pymysql
        mysql_config = {
            "charset": self.kwargs.get('charset', os.getenv('MYSQL_CHARSET', 'utf8mb4')),
            "db": self.kwargs.get('db', os.getenv('MYSQL_DB', 'test')),
            "host": self.kwargs.get('host', os.getenv('MYSQL_HOST', '127.0.0.1')),
            "port": self.kwargs.get('port', os.getenv('MYSQL_PORT', 3306)),
            "user": self.kwargs.get('user', os.getenv('MYSQL_USER', 'dev')),
            "password": self.kwargs.get('password', os.getenv('MYSQL_PASSWORD', 'Devadmin001'))
        }
        self.conn = pymysql.connect(**mysql_config)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def use_mysql_hook_connect(self):
        self.conn = self.mysql_hook.get_conn()
        self.cursor = self.conn.cursor()

    def connect(self):
        if self.mysql_hook:
            self.use_mysql_hook_connect()
        else:
            self.use_pymysql_connect()

    def export(self, **kwargs):
        self.connect()
        self.table = kwargs.get('table')
        sql_rundate = kwargs.get('sql_rundate', "select max(rundate) from {}".format(self.table))
        rundate_db = self.get_rundate(sql_rundate)

        '''
        check rundate part
        '''
        if kwargs.get('schedule_interval') == 'hour':
            rundate_check = rundate_db.strftime('%Y-%m-%d-%H')
        elif kwargs.get('schedule_interval') == 'minute':
            rundate_check = rundate_db.strftime('%Y-%m-%d-%H-%M')
        else:
            rundate_check = rundate_db.strftime('%Y-%m-%d')

        hour_delta = kwargs.get('hour_delta', 0)
        now_time = datetime.datetime.now() + datetime.timedelta(hours=hour_delta)
        if rundate_check not in str(now_time):
            raise ValueError("rundate in db not qualified: db: {} now: {} ".format(rundate_db, now_time))
        else:
            print("rundate qualified: db: {} now: {} ".format(rundate_db, now_time))

        '''
        check insert time part
        '''

        sql_last_insert_time = kwargs.get('sql_rundate', "select tid, InsertUpdateTime from {table} order by 1 desc limit 1".format(table=self.table))
        last_insert_time = self.get_last_insert_time(sql_last_insert_time)
        time_diff = now_time - last_insert_time
        if time_diff.total_seconds() < 5 * 50:
            raise ValueError('insert time does not qualified db: {} now: {} '.format(last_insert_time, now_time))
        else:
            print('insert time qualified db: {} now: {} '.format(last_insert_time, now_time))

        '''
        download file part
        '''

        sql = kwargs.get('sql', '''select * from {table} where rundate = (select max(rundate) from {table} ) '''.format(table=self.table))
        file_type = kwargs.get('file_type', 'csv')
        file_name_template = kwargs.get('file_name_template', '{}_%s'.format(self.table))
        file_name = kwargs.get('file_name', file_name_template % rundate_check)
        if debug():
            file_folder = kwargs.get('file_folder', os.path.join(os.path.expanduser('~'), 'DataExported', self.table))
        else:
            file_folder = kwargs.get('file_folder',  os.path.join(os.path.dirname(inspect.stack()[1][1]), 'Data/'))

        if not os.path.exists(file_folder):
            os.makedirs(file_folder)

        file = os.path.join(file_folder, file_name)
        if file_type == 'csv':
            return self.export_to_csv(sql, file + '.csv')
        else:
            raise ValueError('unknown file type', file_type)

    def export_to_csv(self, sql, file):
        self.cursor.execute(sql)
        fields = [_[0] for _ in self.cursor.description]

        rows = self.cursor.fetchall()

        with open(file, 'w') as fh:
            writer = csv.writer(fh)
            writer.writerow(fields)
            writer.writerows(rows)

        self.conn.close()
        return file

    def export_to_parquet(self, sql, file):
        self.cursor.execute(sql)
        return file

    def get_rundate(self, sql_rundate):
        self.cursor.execute(sql_rundate)
        result = self.cursor.fetchone()
        rundate_db = result[0]
        return rundate_db

    def get_last_insert_time(self, sql_insert_time):
        self.cursor.execute(sql_insert_time)
        last_insert_time = self.cursor.fetchone()[-1]
        return last_insert_time



    def test(self):
        return os.path.join(os.path.dirname(inspect.stack()[1][1]), 'Data/')