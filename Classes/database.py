import sqlite3

from aiogram.types import CallbackQuery
from aiogram import Bot

from .vacancy import CompanyVacancy


class Database:
    def __init__(self, main_bot, db_path: str = 'DataBase/parse_bot_db.db'):
        self.db_path = db_path
        self.bot: Bot = main_bot

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_tables_list(self):
        sql = '''CREATE TABLE IF NOT EXISTS tables_list 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT, table_name TEXT, active INTEGER)'''
        self.execute(sql, commit=True)
        sql = '''CREATE UNIQUE INDEX IF NOT EXISTS company ON tables_list (company)'''
        self.execute(sql, commit=True)

    def create_table(self, company: str):
        sql = f'''CREATE TABLE IF NOT EXISTS table_{company} 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, position TEXT, url TEXT, parse_time TEXT)'''
        self.execute(sql, commit=True)
        sql = f'''CREATE UNIQUE INDEX IF NOT EXISTS position ON table_{company} (position, url)'''
        self.execute(sql, commit=True)
        sql = '''REPLACE INTO tables_list (company, table_name, active) 
        VALUES (?, ?, ?, ?)'''
        self.execute(sql, (company, f'table_{company}', 1), commit=True)

    async def update(self, base: CompanyVacancy, call: CallbackQuery):
        chat_id = call.message.chat.id if isinstance(call, CallbackQuery) else call.chat.id
        message_id = call.message.message_id if isinstance(call, CallbackQuery) else call.message_id
        if isinstance(call, CallbackQuery):
            await self.bot.edit_message_text(text=f'Начали обход {base.company}', chat_id=chat_id,
                                             message_id=message_id)
        else:
            await self.bot.send_message(text=f'Начали обход {base.company}', chat_id=chat_id)
        for vacancy in base.vacancies:
            position, url = vacancy.extract()
            sql = f'''REPLACE INTO {base.table} (position, url) 
                    VALUES (?, ?)'''
            self.execute(sql, (position, url), commit=True)

    def archive(self, vacancy: dict):
        sql = f'''REPLACE INTO table_{vacancy.get('company')} (position, url) VALUES (?, ?)'''
        self.execute(sql, (vacancy.get('name'), vacancy.get('url')), commit=True)

    def check_new(self, base: CompanyVacancy):
        company, table, parse_time = base.database()
        result = []
        for vacancy in base.vacancies:
            position, url = vacancy.extract()
            sql = f'''SELECT * FROM {table} WHERE position=? AND url=?'''
            entry = self.execute(sql, (position, url), fetchone=True)
            if not entry:
                new_entry = {"company": company,
                             "parse_time": parse_time,
                             "name": vacancy.position,
                             "url": vacancy.url}
                result.append(new_entry)
        return result

    def company_list(self) -> list:
        sql = '''SELECT * FROM tables_list'''
        return self.execute(sql, fetchall=True)

    def active_company(self) -> list:
        sql = '''SELECT table_name FROM tables_list WHERE active = 1'''
        return self.execute(sql, fetchall=True)

    def switch_active(self, name):
        sql = f'''UPDATE tables_list SET active = CASE WHEN active = 1
        THEN 0 ELSE 1 END WHERE company=?'''
        self.execute(sql, (name,), commit=True)

    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()
