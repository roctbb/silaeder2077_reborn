from telebot import types
import random


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поиграть на пианино"))
    keyboard.add(types.KeyboardButton(text="Потыкать по доске"))
    bot.send_message(user['id'], 'Вы в каб. 116', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. 116')


def user_message(bot, message, user, location, all_users):
    if message == 'Поиграть на пианино':
        user['energy'] = min(100, user['energy'] - 5)
        user['experience'] = min(100, user['experience'] + 5)
        bot.send_message(user['id'], f'Вы поиграли на пианино'
                                     f'Теперь у вас {user['experience']} опыта и {user['energy']} энергии')
    elif message == 'Потыкать по доске':
        user['energy'] = min(100, user['energy'] - 5)
        bot.send_message(user['id'], f'Вы поиграли на пианино'
                                     f'У вас теперь {user['energy']} энергии, но у вас поднялосб настроение')
        if random.randint(0, 3) == 1:
            bot.send_message(user['id'], f'Вас спалил учитель!!!'
                                         f'И отвели в 105...')

    else:
        bot.send_message(user['id'], 'Я вас не понял :(')
