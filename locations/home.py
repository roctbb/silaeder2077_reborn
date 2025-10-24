from telebot import types
from methods import *


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Пойти в школу!"))
    bot.send_message(user['id'], 'Вы дома! И тут от вашего компьютера слышиться звук, это в нашем тг канале запостили новое сообщение быстрее присоединяйтесь: https://t.me/+tJMzrFckTCUxOTFi', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите их дома')


def user_message(bot, message, user, location, all_users):
    if message == 'Пойти в школу!':
        transfer_user(user, 'yard')
    else:
        bot.send_message(user['id'], 'Я вас не понял')
