import json
import os
from aiogram.types import CallbackQuery

from Classes import CompanyVacancy
from DataBase.JSON import files, new_vac
from Keyboards import kb_link
from Keyboards.callback_data import menu
from loader import dp, db


async def update_db(table_name):
    with open(files.get(table_name), 'r', encoding='UTF-8') as file:
        data = json.load(file)
    await db.update(CompanyVacancy(data))


async def vacancy_seller(call: CallbackQuery, file: CompanyVacancy):
    all_vac_list = db.check_new(file)
    if all_vac_list:
        vac_list = CompanyVacancy(all_vac_list)
        for vac in vac_list.vacancies:
            text = f'Биржа: {vac_list.company}\nОбновление: {vac_list.parse_time}\n\n'
            await call.message.answer(text=text + vac.position,
                                      reply_markup=kb_link(vac.url))
    return all_vac_list


@dp.callback_query_handler(menu.filter(name='link'))
async def com_link(call: CallbackQuery):
    name = call.data.split(';')[-1]
    new_storage = read_new_storage()
    print(f'Читаем {new_storage}')
    if name == 'all':
        company_list = db.active_company()
        paths = [files.get(name[0]) for name in company_list]
    else:
        paths = [files.get(name)]
    if paths:
        for path in paths:
            with open(path, 'r', encoding='UTF-8') as file:
                vac_file = json.load(file)
                com_vacancy = CompanyVacancy(vac_file)
                new_vacancies = await vacancy_seller(call, com_vacancy)
                for vacancy in new_vacancies:
                    if vacancy not in new_storage:
                        print(f'Записываем {vacancy}')
                        new_storage.append(vacancy)
                with open(new_vac, 'w', encoding='UTF-8') as data:
                    json.dump(new_storage, data)
                # await db.update(com_vacancy, call)
    #             for vacancy in new_vacancies:
    #                 new_json[new_id()] = vacancy
    #                 with open(new_vac, 'a', encoding='UTF-8') as new_v:
    #                     json.dump(new_json, new_v)
    # print(new_json)
    await call.message.answer('На данный момент всё')



def read_new_storage():
    if not os.path.exists(new_vac):
        with open(new_vac, 'w', encoding='UTF-8') as file:
            new_storage = []
            json.dump(new_storage, file)
    with open(new_vac, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data

# def new_id() -> int:
#     file = read_new_json()
#     return (max([int(key) for key in file])) + 1 if file else 1