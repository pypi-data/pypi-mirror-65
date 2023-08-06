import os
import mysql.connector
import psycopg2 as psycopg2

from Resources.helper.BaseActions import BaseActions
from Resources.helper.Utils import connect_to_okd
from Variables.main_vars import *


class DatabaseManager(BaseActions):
    def __init__(self):
        super().__init__()
        self.my_db = None
        self.my_cursor = None
        self.postgres_db = None
        self.postgres_cursor = None

    def query_runner(self, query):
        query = query.lstrip()
        result = None
        self.connect_to_data_base()
        self.my_cursor.execute(query)
        if query.lower().startswith('select'):
            result = self.my_cursor.fetchall()
        else:
            self.my_db.commit()
        self.close_connection()
        return result

    def postgres_query_runner(self, db_name, query):
        query = query.lstrip()
        print(query)
        result = None
        self.connect_to_postgres(db_name)
        self.postgres_cursor.execute(query)
        if query.lower().startswith('select'):
            result = self.postgres_cursor.fetchall()
        else:
            self.postgres_db.commit()
        self.close_postgres_connection()
        return result

    @staticmethod
    def mysql_port_forward():
        os.system("oc port-forward dc/mysqlcentral 3306:3306 > /dev/null 2>&1  &")

    @staticmethod
    def postgres_port_forward(db_name):
        port = '5433'
        if db_name == 'rasoul':
            port = '5434'
        os.system('oc port-forward dc/{}-postgresql {}:5432 > /dev/null 2>&1  &'.format(db_name, port))

    def connect_to_postgres(self, db_name, retry=True):
        try:
            port = 5433
            if db_name == 'rasoul':
                port = 5434
            self.postgres_db = psycopg2.connect(host=DBHost, database=db_name, user="postgres",
                                                password=db_name, port=port)
            self.postgres_cursor = self.postgres_db.cursor()
        except Exception as e:
            if retry:
                self.bi.log_to_console(e)
                connect_to_okd()
                self.postgres_port_forward(db_name)
                self.connect_to_postgres(db_name=db_name, retry=False)
            raise Exception(e)

    def connect_to_data_base(self, retry=True):
        try:
            self.my_db = mysql.connector.connect(
                host=DBHost,
                port=DBPort,
                user=DBUser,
                passwd="",
            )
            self.my_cursor = self.my_db.cursor()
        except Exception as e:
            if retry:
                self.bi.log_to_console(e)
                connect_to_okd()
                self.mysql_port_forward()
                self.connect_to_data_base(retry=False)
            raise Exception(e)

    def close_connection(self):
        self.my_db.close()

    def close_postgres_connection(self):
        self.postgres_db.close()
