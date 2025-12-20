from telebot import types
from datetime import datetime
import random
from methods import *

def user_enters_location(bot, user, location, all_users):
    c_time = datetime.now()
    c = False
    if (c_time.hour == 10 and 46 > c_time.minute > 24) or (c_time.hour == 13 and 51 > c_time.minute > 9):
        c = True

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Покушать пельмешки"))
    keyboard.add(types.KeyboardButton(text="Попить чай"))
    keyboard.add(types.KeyboardButton(text="Украсть ложку"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. 105"))

    if c:
        send_photo(bot, user['id'], 'assets/images/stolovka.jpg', 'Вы в столовой', reply_markup=keyboard)
    else:
        send_photo(bot, user['id'], 'assets/images/stolovka.jpg', 'Вас выгнали, ведь сейчас не время кушать',
                   reply_markup=keyboard)
        transfer_user(user, 'hall')


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете столовую')


def user_message(bot, message, user, location, all_users):
    n = random.randint(1, 10)
    q = random.randint(1, 10)

    c_time = datetime.now()
    c = False
    if (c_time.hour == 10 and 46 > c_time.minute > 24) or (c_time.hour == 13 and 51 > c_time.minute > 9):
        c = True

    if message == 'Покушать пельмешки':
        if c:
            if n == 1:  # Пельмени с истекшим сроком годности
                user['food'] = max(0, user['food'] - 15)
                bot.send_message(user['id'], f'Вы перекусили пельменями с закончившимся сроком годности. '
                                             f'Теперь у вас {user["food"]} сытости.')
            else:  # Обычные пельмени
                user['food'] = min(100, user['food'] + 15)
                bot.send_message(user['id'], f'Вы перекусили пельменями. '
                                             f'Теперь у вас {user["food"]} сытости.')
        else:
            bot.send_message(user['id'], 'Вас выгнали из столовой, ведь сейчас не время кушать')
            transfer_user(user, 'hall')

    elif message == 'Попить чай':
        if c:
            user['water'] = min(100, user['water'] + 15)
            bot.send_message(user['id'], f'Вы попили чай. '
                                         f'Теперь у вас {user["water"]} очков жажды.')
        else:
            bot.send_message(user['id'], 'Вас выгнали из столовой, ведь сейчас не время кушать')
            transfer_user(user, 'hall')

    elif message == 'Украсть ложку':
        if c:
            if q != 1:
                bot.send_message(user['id'], 'Никто не заметил пропажи ложки')
                user['inventory'].append('spoon')
            else:
                bot.send_message(user['id'], 'Повариха заметила пропажу ложки и вас отправили в 105 кабинет')
                user["ochota"] = 2
                transfer_user(user, 'room105')
        else:
            bot.send_message(user['id'], 'Вас выгнали из столовой, ведь сейчас не время кушать')
            transfer_user(user, 'hall')
    else:
        bot.send_message(user['id'], 'Я вас не понял')


