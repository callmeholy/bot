import telebot
from telebot import types
from get_weather import get_weather, get_weather_for_5_days, get_weather_all_day
from tokens import bot_token, open_weather_token
bot = telebot.TeleBot(bot_token)

list_of_req = []


@bot.message_handler(commands=['start'])
def command_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Узнать погоду в городе сейчас', callback_data='print_weather'))
    markup.add(types.InlineKeyboardButton('Узнать погоду на сегодня', callback_data='weather_all_day'))
    markup.add(types.InlineKeyboardButton('Узнать погоду на 5 дней', callback_data='weather_5'))
    markup.add(types.InlineKeyboardButton('История запросов', callback_data='history'))
    bot.send_message(message.chat.id, 'Привет, я бот который поможет узнать погоду в любом городе!',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'print_weather':
        bot.send_message(callback.message.chat.id, 'Введите город в котором хотите узнать погоду:')
        bot.register_next_step_handler(callback.message, print_weather)
    elif callback.data == 'history':
        history(callback.message)
    elif callback.data == 'main_menu':
        command_start(callback.message)
    elif callback.data == 'weather_5':
        bot.send_message(callback.message.chat.id, 'Введите город в котором хотите узнать погоду:')
        bot.register_next_step_handler(callback.message, weather_for_5_days)
    elif callback.data == 'weather_all_day':
        bot.send_message(callback.message.chat.id, 'Введите город в котором хотите узнать погоду:')
        bot.register_next_step_handler(callback.message, print_weater_all_day)


def weather_for_5_days(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Назад в меню', callback_data='main_menu'))
    try:
        cur_city = message.text
        bot.send_message(message.chat.id, 'Данные загружаются...')
        result = get_weather_for_5_days(cur_city, open_weather_token)
        chek_data = 0
        main_answer = f''
        for key, value in result.items():
            if chek_data == key[8:10]:
                main_answer += f'{key[11:]} {value}C°\n'
            else:
                chek_data = key[8:10]
                main_answer += f'<b>{key[:10]}</b>\n{key[11:]} {value}C°\n'
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, main_answer, parse_mode='html', reply_markup=markup)
        if len(list_of_req) >= 5:
            list_of_req.remove(list_of_req[0])
        list_of_req.append(cur_city)
    except Exception:
        bot.delete_message(message.chat.id, message.message_id + 1)
        markup.add(types.InlineKeyboardButton('Ввести город еще раз', callback_data='weather_5'))
        bot.send_message(message.chat.id, 'Такого города я не знаю, Хотите ввести город еще раз?', reply_markup=markup)


def print_weather(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Назад в меню', callback_data='main_menu'))
    try:
        cur_city = message.text
        bot.send_message(message.chat.id, 'Данные загружаются...')
        result = get_weather(cur_city, open_weather_token)
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, f''
                                          f'Город: <b>{cur_city}</b>\nТемпература: <b>{result["cur_temp"]} градусов</b>\n'
                                          f'Ощущается как: <b>{result["feels_like"]} градусов</b>\nСкорость ветра: '
                                          f'<b>{result["wind_speed"]}м/c</b> \nОписание погоды:'
                                          f' <b>{result["description"]}</b>', parse_mode='html', reply_markup=markup)
        if len(list_of_req) >= 5:
            list_of_req.remove(list_of_req[0])
        list_of_req.append(cur_city)
    except Exception:
        bot.delete_message(message.chat.id, message.message_id + 1)
        markup.add(types.InlineKeyboardButton('Ввести город еще раз', callback_data='print_weather'))
        bot.send_message(message.chat.id, 'Такого города я не знаю, Хотите ввести город еще раз?', reply_markup=markup)


def print_weater_all_day(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Назад в меню', callback_data='main_menu'))
    try:
        cur_city = message.text
        bot.send_message(message.chat.id, 'Данные загружаются...')
        result = get_weather_all_day(cur_city, open_weather_token)
        main_answer = f'Погода на сегодня:\n'
        for key, value in result.items():
            main_answer += f'{key} {value}C°\n'
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, main_answer, parse_mode='html', reply_markup=markup)
        if len(list_of_req) >= 5:
            list_of_req.remove(list_of_req[0])
        list_of_req.append(cur_city)
    except Exception:
        bot.delete_message(message.chat.id, message.message_id + 1)
        markup.add(types.InlineKeyboardButton('Ввести город еще раз', callback_data='weather_5'))
        bot.send_message(message.chat.id, 'Такого города я не знаю, Хотите ввести город еще раз?', reply_markup=markup)


def history(message):
    if len(list_of_req) == 0:
        bot.send_message(message.chat.id, 'Список истории пуст')
    else:
        ans = ', '.join(list_of_req)
        bot.send_message(message.chat.id, f'Вот список последних запросов: {ans}')


@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, 'Я вас не понял, введите комману "/start", чтобы узнать мой функционал.')


bot.polling(none_stop=True)