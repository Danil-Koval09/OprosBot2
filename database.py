import sqlite3
import pandas as pd


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('anketa.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            full_name TEXT,
            gender TEXT,
            age INTEGER,
            phone TEXT,
            payment TEXT

        )
        '''

        self.manager(sql, commit=True)

    def get_user_by_chat_id(self, chat_id):
        sql = '''
        SELECT * FROM users WHERE chat_id = ?
        '''
        return self.manager(sql, chat_id, fetchone=True)

    def first_registration_user(self, chat_id):
        sql = '''
        INSERT INTO users(chat_id) VALUES (?)
        '''
        self.manager(sql, chat_id, commit=True)

    def update_data(self, chat_id, full_name, gender, age, phone, payment):
        sql = '''
        UPDATE users
        SET full_name = ?,
        gender = ?,
        age = ?,
        phone = ?,
        payment = ?
        WHERE chat_id = ?
        '''
        self.manager(sql, full_name, gender, age, phone, payment, chat_id, commit=True)

    def get_data_for_excel(self):
        sql = '''SELECT * FROM users'''
        df = pd.read_sql_query(sql, self.database)
        df.to_excel('result.xlsx', index=False, engine='openpyxl')
