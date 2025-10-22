from telebot import types
import random

def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Взять туалетную бумагу"))
    keyboard.add(types.KeyboardButton(text="Бросить туалетную бумагу"))
    keyboard.add(types.KeyboardButton(text="Перейти в двор"))
    bot.send_message(user['id'], 'Вы вошли в туалет', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы вышли из туалета')


def user_message(bot, message, user, location, all_users):
    if message == 'Бросить туалетную бумагу':
        if user['energy'] > 15:
            user['energy'] = min(100, user['energy'] - 15)
            bot.send_message(user['id'], f'Вы бросили туалетную бумагу, вам бросили её в ответ. Так вы кидались нессколько минут. \nТеперь у вас {user['energy']} энергии.')
        else:
            bot.send_message(user['id'], f'У вас недостаточно энергии, чтобы сделать это. \nУ вас {user['energy']} энергии.')
    elif message == 'Взять туалетную бумагу':
        bot.send_message(user['id'], f'Вы украли туалетную бумагу, ведь вам нужнее')
        user['inventory'].append('toilet_paper')
    else:
        bot.send_message(user['id'], 'Я вас не понял')

