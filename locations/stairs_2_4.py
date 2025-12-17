from telebot import types
from methods import *


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Переход: холл 2 этажа"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 4 этажа"))

    bot.send_message(user['id'],
                     'Вы на лестнице со 2 на 4 этаж.',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите с лестницы')


def user_message(bot, message, user, location, all_users):
    if message.startswith('Переход: '):
        location_name = message.replace('Переход: ', '')

        if location_name == 'холл 2 этажа':
            transfer_user(user, 'hall_2')
        elif location_name == 'холл 4 этажа':
            transfer_user(user, 'hall_4')
        else:
            bot.send_message(user['id'], 'Отсюда можно пойти только в холл 2 или 4 этажа')
    else:
        bot.send_message(user['id'], 'Я вас не понял')