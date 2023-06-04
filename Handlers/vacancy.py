import json

from aiogram.types import CallbackQuery

from Classes import CompanyVacancy
from DataBase.JSON import files
from Keyboards import kb_link
from Keyboards.callback_data import menu
from loader import dp, db


async def update_db(table_name):
    with open(files.get(table_name), 'r', encoding='UTF-8') as file:
        data = json.load(file)
    await db.update(CompanyVacancy(data))


async def vacancy_seller(call: CallbackQuery, file: CompanyVacancy):
    vac_list = db.check_new(file)
    if vac_list:
        vac_list = CompanyVacancy(vac_list)
        for vac in vac_list.vacancies:
            text = f'Биржа: {vac_list.company}\nОбновление: {vac_list.parse_time}\n\n'
            print(vac)
            await call.message.answer(text=text + vac.position,
                                      reply_markup=kb_link(vac.url))


@dp.callback_query_handler(menu.filter(name='link'))
async def com_link(call: CallbackQuery):
    name = call.data.split(':')[-1]
    if name == 'all':
        # with open('DataBase/files_list.ini', 'r', encoding='UTF-8') as file:
        company_list = db.active_company()
        paths = [files.get(name[0]) for name in company_list]
    else:
        paths = [files.get(name)]
    if paths:
        for path in paths:
            with open(path, 'r', encoding='UTF-8') as file:
                vac_file = json.load(file)
                com_vacancy = CompanyVacancy(vac_file)
                await vacancy_seller(call, com_vacancy)
                await db.update(com_vacancy, call)
    await call.message.answer('На данный момент всё')