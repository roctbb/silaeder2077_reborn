from telebot import types
from methods import *


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 2 этажа"))

    bot.send_message(user['id'],
                     'Вы на лестнице с 1 на 2 этаж.',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите с лестницы')


def user_message(bot, message, user, location, all_users):
    if message.startswith('Переход: '):
        location_name = message.replace('Переход: ', '')

        if location_name == 'холл 1 этажа':
            transfer_user(user, 'hall_1')
        elif location_name == 'холл 2 этажа':
            transfer_user(user, 'hall_2')
        else:
            bot.send_message(user['id'], 'Отсюда можно пойти только в холл 1 или 2 этажа')
    else:
        bot.send_message(user['id'], 'Я вас не понял')