import aiogram

#Создаем кнопку старта
but_start = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
start = aiogram.types.KeyboardButton('СТАРТ')
but_start.add(start)

#Создаем кнопки главного меню
but_handler_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
choise = aiogram.types.KeyboardButton('Ввести страну')
favourite = aiogram.types.KeyboardButton('Избранное')
info = aiogram.types.KeyboardButton('Инструкция пользования')
exit = aiogram.types.KeyboardButton('Выйти')
but_handler_menu.row(choise, favourite).row(info, exit)

#Создаем кнопки назад и выйти
but_exit = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
nazad = aiogram.types.KeyboardButton('Назад')
exit = aiogram.types.KeyboardButton('Выйти')
but_exit.row(nazad, exit)

#Создаем кнопки главное меню и выйти
but_main = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu = aiogram.types.KeyboardButton('Вернуться в меню')
add = aiogram.types.KeyboardButton('Добавить в избранное')
but_main.add(add).row(main_menu, exit)

#Инструкция пользования
information = '''Привет! Я - бот погоды и времени. Вы можете узнать погоду и время в любой точке мира на текущий момент! Здорово, правда?!

\U0001F539 Для удобства созданы специальные кнопки - нажимайте на них и будем вам счастье :)
\U0001F539 Сначала введите страну, а затем населённый пункт, где хотите посмотреть погоду и время.
\U0001F539 Вы также можете добавить населённый пункт в избранное для быстрого доступа.
\U0001F539 Удалить населенный пункт из списка "Избранное" можно только по требованию, поэтому постарайтесь не засорять данный список.
\U0001F539 Как заканчиваете общение со мной, нажимайте кнопку 'Выйти'.
\U0001F539 Если я не реагирую на команды, разбудите меня командой '/start', введённой вручную.

Если возникнут трудности, пишите моему создателю - @be9emot.'''