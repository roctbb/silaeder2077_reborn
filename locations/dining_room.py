from telebot import types
from datetime import datetime
import random


def user_enters_location(bot, user, location, all_users):
    n = random.randint(1, 10)

    c_time = datetime.now()
    c = False
    if (c_time.hour == 10 and 46 > c_time.minute > 24) or (c_time.hour == 13 and 51 > c_time.minute > 9):
        c = True

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Покушать пельмешки"))
    keyboard.add(types.KeyboardButton(text="Перейти в холл"))
    if c == True:
        bot.send_message(user['id'], 'Вы в столовой', reply_markup=keyboard)
    else:
        bot.send_message(user['id'], 'Вас выгнали,ведь сейчас не время кушать', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете столовую')


def user_message(bot, message, user, location, all_users):
    n = random.randint(1, 10)

    c_time = datetime.now()
    c = False
    if (c_time.hour == 10 and 46 > c_time.minute > 24) or (c_time.hour == 13 and 51 > c_time.minute > 9):
        c = True

    if message == 'Покушать пельмешки' and c == True:
        user['food'] = min(100, user['food'] + 15)
        user['water'] = min(100, user['water'] + 15)
        bot.send_message(user['id'], f'Вы перекусили пельменями. '
                                     f'Теперь у вас {user["food"]} сытости.')
    elif message == 'Покушать пельмешки' and c == True and n == 1:
        user['food'] = max(0, user['food'] - 15)
        user['water'] = max(0, user['water'] - 15)
        bot.send_message(user['id'], f'Вы перекусили пельменями с закончившимся сроком годности '
                                     f'Теперь у вас {user["food"]} сытости.')
    elif message == 'Покушать пельмешки' and c == False:
        bot.send_message(user['id'], 'Вас выпинали из столовой')
    else:
        bot.send_message(user['id'], 'Я вас не понял')
