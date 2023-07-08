import json
import os

from aiogram.types import CallbackQuery

from Classes import CompanyVacancy
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
        for index, vacancy in enumerate(vac_list.vacancies):
            text = f'Биржа: {vacancy.get("company")}\nОбновление: {vacancy.get("parse_time")}\n\n'
            await call.message.answer(text=text + vacancy.get("name"),
                                      reply_markup=kb_link(vacancy.get("name"), index))
    return all_vac_list


@dp.callback_query_handler(menu.filter(name='link'))
async def show_vacancy(call: CallbackQuery):
    with open(new_vac, 'r', encoding='UTF-8') as file:
        vacancies = json.load(file)
    if vacancies:
        for index, vacancy in enumerate(vacancies):
            text = f'Биржа: {vacancy.get("company")}\nОбновление: {vacancy.get("parse_time")}\n\n'
            await call.message.answer(text=text + vacancy.get("name"),
                                      reply_markup=kb_link(vacancy.get("url"), index))


# @dp.callback_query_handler(menu.filter(name='link'))
# async def collect_new(call: CallbackQuery):
#     name = call.data.split(';')[-1]
#     new_storage = read_new_storage()
#     if name == 'all':
#         company_list = db.active_company()
#         paths = [files.get(name[0]) for name in company_list]
#     else:
#         paths = [files.get(name)]
#     if paths:
#         for path in paths:
#             with open(path, 'r', encoding='UTF-8') as file:
#                 vac_file = json.load(file)
#                 com_vacancy = CompanyVacancy(vac_file)
#                 new_vacancies = await vacancy_seller(call, com_vacancy)
#                 for vacancy in new_vacancies:
#                     if vacancy not in new_storage:
#                         new_storage.append(vacancy)
#                 with open(new_vac, 'w', encoding='UTF-8') as data:
#                     json.dump(new_storage, data, indent=4, ensure_ascii=False)
#                 # await db.update(com_vacancy, call)
#     #             for vacancy in new_vacancies:
#     #                 new_json[new_id()] = vacancy
#     #                 with open(new_vac, 'a', encoding='UTF-8') as new_v:
#     #                     json.dump(new_json, new_v)
#     # print(new_json)
#     await call.message.answer('На данный момент всё')

@dp.callback_query_handler(menu.filter(name='link'))
async def show_new(call: CallbackQuery):
    index = call.data.split(';')[-1]
    if new_storage := read_new_storage():
        for vacancy in new_storage:
            with open(path, 'r', encoding='UTF-8') as file:
                vac_file = json.load(file)
                com_vacancy = CompanyVacancy(vac_file)
                new_vacancies = await vacancy_seller(call, com_vacancy)
                for vacancy in new_vacancies:
                    if vacancy not in new_storage:
                        new_storage.append(vacancy)
                with open(new_vac, 'w', encoding='UTF-8') as data:
                    json.dump(new_storage, data, indent=4, ensure_ascii=False)
                # await db.update(com_vacancy, call)
    #             for vacancy in new_vacancies:
    #                 new_json[new_id()] = vacancy
    #                 with open(new_vac, 'a', encoding='UTF-8') as new_v:
    #                     json.dump(new_json, new_v)
    # print(new_json)
    await call.message.answer('На данный момент всё')


def collect_new():
    new_storage = read_new_storage()
    company_list = db.active_company()
    paths = [files.get(name[0]) for name in company_list]
    for path in paths:
        with open(path, 'r', encoding='UTF-8') as file:
            vac_file = json.load(file)
        new_vacancies = db.check_new(CompanyVacancy(vac_file))
        for vacancy in new_vacancies:
            if vacancy not in new_storage:
                new_storage.append(vacancy)
    with open(new_vac, 'w', encoding='UTF-8') as data:
        json.dump(new_storage, data, indent=4, ensure_ascii=False)


def read_new_storage():
    if not os.path.exists(new_vac):
        with open(new_vac, 'w', encoding='UTF-8') as file:
            new_storage = []
            json.dump(new_storage, file)
    with open(new_vac, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data


@dp.callback_query_handler(menu.filter(name='del_vac'))
async def delete_vacancy(call: CallbackQuery):
    index = int(call.data.split(';')[-1])
    new_storage = read_new_storage()
    temp_vacancy = new_storage.pop(index)
    db.archive(temp_vacancy)
    with open(new_vac, 'w', encoding='UTF-8') as file:
        json.dump(new_storage, file, indent=4, ensure_ascii=False)
    await call.message.delete()
