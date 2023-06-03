import sqlite3

from .vacancy import CompanyVacancy


class Database:
    def __init__(self, db_path: str = 'DataBase/parse_bot_db.db'):
        self.db_path = db_path

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
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT, table_name TEXT, parse_time TEXT, active TEXT)'''
        self.execute(sql, commit=True)
        sql = '''CREATE UNIQUE INDEX IF NOT EXISTS company ON tables_list (company)'''
        self.execute(sql, commit=True)

    def create_table(self, company: str, table: str, parse_time: str):
        sql = f'''CREATE TABLE IF NOT EXISTS {table} 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, position TEXT, url TEXT)'''
        self.execute(sql, commit=True)
        sql = '''REPLACE INTO tables_list (company, table_name, parse_time) VALUES (?, ?, ?)'''
        self.execute(sql, (company, table, parse_time), commit=True)

    def fill_table(self, base: CompanyVacancy):
        company, table, parse_time = base.database()
        self.create_table(company, table, parse_time)
        for vacancy in base.vacancies:
            position, url = vacancy.extract()
            sql = f'''INSERT INTO {table} (position, url) 
                    VALUES (?, ?)'''
            self.execute(sql, (position, url), commit=True)

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
        return CompanyVacancy(result)

    def company_list(self) -> list:
        sql = '''SELECT * FROM tables_list'''
        return self.execute(sql, fetchall=True)

    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()
