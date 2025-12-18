from telebot import types
from methods import transfer_user
import random


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Постучать и убежать"))
    keyboard.add(types.KeyboardButton(text="Зайти и что нибудь сделать"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    bot.send_message(user['id'], 'Вы пришли к комнате охраны', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули комнату охраны')


def user_message(bot, message, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message == 'Постучать и убежать':
        bot.send_message(user['id'], f'Вы постучали, но из-за двери выходит охраник и забирает в свою подсобку')
        user.remove(user)
        bot.send_message(user['id'], f'Вы умерли.')
        return
    elif message == 'Зайти и что нибудь сделать':
        keyboard.add(types.KeyboardButton(text="Взять броню"))
        keyboard.add(types.KeyboardButton(text="Взять оружие"))
        keyboard.add(types.KeyboardButton(text="попить странную жижу в стакане"))
        keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
        bot.send_message(user['id'], 'Вы зашли в комнату охраны', reply_markup=keyboard)
    elif message == 'Взять броню':
        if 'armor' in location['inventory']:
            location['inventory'].remove('armor')
            user['inventory'].append('armor')
            bot.send_message(user['id'], 'Вы взяли броню', reply_markup=keyboard)
        else:
            bot.send_message(user['id'], 'Брони не осталось', reply_markup=keyboard)
    elif message == 'Взять оружие':
        bot.send_message(user['id'], "Что у вас за мысли?\nВ 105!")
        user['ochota'] = 2
        transfer_user(user, 'room105')
    elif message == 'попить странную жижу в стакане':
        user['energy'] += 250
        if random.randint(0, 3) == 1:
            if 'armor' in user['inventory']:
                bot.send_message(user['id'], f'Вас спалил учитель!!!')
                bot.send_message(user['id'], f'По вам начали стрелять')
                bot.send_message(user['id'], f'вы чудом спаслись')
                user['inventory'].remove('armor')
            elif 'gun' in user['inventory']:
                bot.send_message(user['id'], f'Вас спалил учитель!!!')
                bot.send_message(user['id'], f'Вы отстрелялись на время')
                bot.send_message(user['id'], f'вы чудом спаслись')
                user['inventory'].remove('gun')
            else:
                bot.send_message(user['id'], f'Вас спалил учитель!!!')
                bot.send_message(user['id'], f'Время написать объяснительную')

    else:
        bot.send_message(user['id'], 'Я вас не понял :(')