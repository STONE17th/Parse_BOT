import json

from Classes import CompanyVacancy
from loader import db


def install_db():
    db.create_tables_list()
    for path in all_files:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        db.fill_table(CompanyVacancy(data))


# def open_file(path_file: str):
#     with open(path_file, 'r', encoding='UTF-8') as file:
#         data = json.load(file)
#     return data
#
#
# epam = CompanyVacancy(open_file(path))
# db = database.DataBase()


# db.create_tables_list()
# db.fill_table(epam)

def check():
    return db.check_new(epam)
