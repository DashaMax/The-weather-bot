import aiogram
import pymysql
import ast
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

from BUTS import but_start, but_handler_menu, but_exit, but_main, exit, nazad, information
from admin import host, port, user, password, bot, dp
from def_url import text_weather_time

connection = pymysql.connect(host = host, port = port, user = user,
                             password = password, database = 'city', cursorclass = pymysql.cursors.DictCursor)
cursor = connection.cursor()
table = 'CREATE TABLE IF NOT EXISTS `favourite city`(`N` INT AUTO_INCREMENT, `id` INT NOT NULL, ' \
        '`city` VARCHAR(128) NOT NULL, `email` VARCHAR(128) NOT NULL, PRIMARY KEY(`N`))'
cursor.execute(table)

class dialog(StatesGroup):
    START = State()
    menu = State()
    exit_info = State()
    country_state = State()
    city_state = State()
    finish_state = State()
    fav_city_state = State()

@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Нажмите кнопку СТАРТ, и мы начнем.', reply_markup=but_start)
    await dialog.START.set()

@dp.message_handler(state=dialog.START)
async def START(message: aiogram.types.Message):
    id_user = message.from_user.id

    '''Очистить список избранное'''
    # delete_all = f'DELETE FROM `favourite city` WHERE id = {id_user}'
    # cursor.execute(delete_all)
    # connection.commit()

    '''Удалить населенный пункт из избранного'''
    # delete = f"DELETE FROM `favourite city` WHERE id = {id_user} AND city = 'краснодар'"
    # cursor.execute(delete)
    # connection.commit()

    if message.text == 'СТАРТ':
        await bot.send_message(message.from_user.id, 'Привет! Узнаем погоду?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    else:
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

@dp.message_handler(state=dialog.menu)
async def info(message: aiogram.types.Message):

    if message.text == 'Инструкция пользования':
        await bot.send_message(message.from_user.id, information, reply_markup=but_exit)
        await dialog.exit_info.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    elif message.text == 'Ввести страну':
        await bot.send_message(message.from_user.id, 'Введите страну.', reply_markup=but_exit)
        await dialog.country_state.set()

    elif message.text == 'Избранное':
        id_user = message.from_user.id
        select = f'SELECT city FROM `favourite city` WHERE id = {id_user}'
        cursor.execute(select)
        list_city = cursor.fetchall()

        if list_city == ():
            await bot.send_message(message.from_user.id, 'Вы ещё не добавили ничего в избранное.', reply_markup=but_exit)
            await dialog.exit_info.set()

        else:
            global cities
            cities = []
            global but_love
            but_love = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)

            for el in list_city:
                cities.append(el['city'].capitalize())
                but = aiogram.types.KeyboardButton(el['city'].capitalize())
                but_love.add(but)
            but_love.row(nazad, exit)
            await bot.send_message(message.from_user.id, 'Выберите населенный пункт.', reply_markup=but_love)
            await dialog.fav_city_state.set()

    else:
        await bot.send_message(message.from_user.id, 'Я вас не понял! Выберите действие.', reply_markup=but_handler_menu)
        await dialog.menu.set()

@dp.message_handler(state=dialog.exit_info)
async def exit_info(message: aiogram.types.Message):

    if message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Давайте посмотрим погоду.', reply_markup=but_handler_menu)
        await dialog.menu.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    else:
        await bot.send_message(message.from_user.id, 'Я вас не понял! Выберите действие.', reply_markup=but_exit)
        await dialog.exit_info.set()

@dp.message_handler(state=dialog.fav_city_state)
async def fav_city(message: aiogram.types.Message):

    if message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Посмотрим погоду?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    elif message.text in cities:
        id_user = message.from_user.id
        select_email = f"SELECT email FROM `favourite city` WHERE id = {id_user} AND city = '{message.text}'"
        cursor.execute(select_email)
        list_email = cursor.fetchall()
        await bot.send_message(message.from_user.id, text_weather_time(list_email[0]['email']), reply_markup=but_handler_menu)
        await bot.send_message(message.from_user.id, 'Что теперь?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    else:
        await bot.send_message(message.from_user.id, 'Я вас не понял! Выберите действие.', reply_markup=but_love)
        await dialog.fav_city_state.set()

@dp.message_handler(state=dialog.country_state)
async def country_from_user(message: aiogram.types.Message):

    if message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Что будем делать?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    else:
        file = open('Cities.txt', 'r', encoding='utf-8')
        dict = ast.literal_eval(file.read())
        global country
        country = message.text.lower()

        if country in dict:
            await bot.send_message(message.from_user.id, 'Введите населённый пункт.', reply_markup=but_exit)
            await dialog.city_state.set()

        else:
            await bot.send_message(message.from_user.id, 'Страна введена некорректно. Попробуйте ещё раз.', reply_markup=but_exit)
            await dialog.country_state.set()

        file.close()

@dp.message_handler(state=dialog.city_state)
async def city_from_user(message: aiogram.types.Message):

    if message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Введите страну.', reply_markup=but_exit)
        await dialog.country_state.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    else:
        id_user = message.from_user.id
        file = open('Cities.txt', 'r', encoding='utf-8')
        dict = ast.literal_eval(file.read())
        global city
        city = message.text.lower()

        if city in dict[country]:
            global url_res
            url_res = dict[country][city]
            await bot.send_message(message.from_user.id, text_weather_time(url_res), reply_markup=aiogram.types.ReplyKeyboardRemove())
            select_city = f'SELECT city from `favourite city` WHERE id = {id_user}'
            cursor.execute(select_city)
            city_fav = cursor.fetchall()
            fav_list = []
            for el in city_fav:
                fav_list.append(el['city'])
            if city not in fav_list:
                await bot.send_message(message.from_user.id, 'Если будете часто смотреть погоду в данном населённом пункте, можете добавить его в избранное для быстрого доступа.', reply_markup=but_main)
                await dialog.finish_state.set()
            else:
                await bot.send_message(message.from_user.id, 'Что теперь?', reply_markup=but_handler_menu)
                await dialog.menu.set()

        else:
            await bot.send_message(message.from_user.id, 'Вы ввели населённый пункт некорректно. Попробуйте ещё раз.', reply_markup=but_exit)
            await dialog.city_state.set()

        file.close()

@dp.message_handler(state=dialog.finish_state)
async def finish(message: aiogram.types.Message):

    if message.text == 'Вернуться в меню':
        await bot.send_message(message.from_user.id, 'Посмотрим погоду ещё раз?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    elif message.text == 'Выйти':
        await bot.send_message(message.from_user.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        await dialog.START.set()

    elif message.text == 'Добавить в избранное':
        id_user = int(message.from_user.id)
        insert = f"INSERT INTO `favourite city` (id, city, email) VALUES ({id_user}, '{city}', '{url_res}')"
        cursor.execute(insert)
        connection.commit()
        await bot.send_message(message.from_user.id, 'Что теперь?', reply_markup=but_handler_menu)
        await dialog.menu.set()

    else:
        await bot.send_message(message.from_user.id, 'Я вас не понял. Выберите, что будем делать.', reply_markup=but_main)
        await dialog.finish_state.set()

executor.start_polling(dp, skip_updates=True)


