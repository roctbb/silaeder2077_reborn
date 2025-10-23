from telebot import types
import random
from methods import *


def make_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Переход: каб. 116'))
    keyboard.add(types.KeyboardButton(text="Переход: каб. 105"))
    keyboard.add(types.KeyboardButton(text="Переход: спортзал"))
    keyboard.add(types.KeyboardButton(text="Переход: столовая"))
    keyboard.add(types.KeyboardButton(text="Переход: туалет"))
    keyboard.add(types.KeyboardButton(text="Переход: двор"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. Физики"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. Математики"))
    keyboard.add(types.KeyboardButton(text="Переход: задний двор"))
    keyboard.add(types.KeyboardButton(text="Переход: дом"))

    return keyboard


def user_enters_location(bot, user, location, all_users):
    if 'card' in user['inventory']:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Пойти в потеряшки, может найду что нибудь интересное."))
        keyboard.add(types.KeyboardButton(text="Накричать на охранника."))
        keyboard.add(types.KeyboardButton(text="Просто пойти дальше."))
        bot.send_message(user['id'], 'Вы входите в холл, что вы будете делать?', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Попробовать убежать."))
        keyboard.add(types.KeyboardButton(text="Пойти в 105 взять карточку."))
        bot.send_message(user['id'],
                         'У вас нет карточки по этому вы подходите к охранникам и записываетесь, что вы будете делать?',
                         reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из холла')


def user_message(bot, message, user, location, all_users):
    if message == 'Пойти в потеряшки, может найду что нибудь интересное.':
        user['energy'] = max(0, user['energy'] - 5)
        if random.randint(1,10) < 5:
            user['food'] = min(100, user['food'] + random.randint(1, 15))
            bot.send_message(user['id'], f'Вы покопались в потеряшках, Теперь у вас {user["energy"]} энергии и {user["food"]} еды')
            bot.send_message(user['id'],'Вы нашли кусок хлеба сьели, но вы услышали шаги разгневанной Инги Александровны и решили сбежать')
        else:
            user['water'] = min(100, user['water'] + random.randint(1, 15))
            bot.send_message(user['id'],f'Вы покопались в потеряшках, Теперь у вас {user["energy"]} энергии и {user["water"]} воды')
            bot.send_message(user['id'],'Вы нашли бутылку воды и выпили её, но вы услышали шаги разгневанной Инги Александровны и решили сбежать')
        bot.send_message(user['id'], 'Куда вы убежите!', reply_markup=make_default_keyboard())

    elif message == 'Попробовать убежать.':
        if random.randint(1, 10) > 5:
            bot.send_message(user['id'], 'Вас хватают и уводят в 105')
            transfer_user(user, 'room105')
        else:
            bot.send_message(user['id'], 'Убегая вы понимаете что нужно спрятаться в одном из кабинетов!',
                             reply_markup=make_default_keyboard())
    elif message == "Накричать на охранника.":
        bot.send_message(user['id'], 'Охранник приходит в бешенство, бежит к тебе и отводит в 105.')
        transfer_user(user, 'room105')
    elif message == "Пойти в 105 взять карточку.":
        bot.send_message(user['id'],
                         'Слава богу в этот раз ты идешь в 105 просто за карточкой, а не за объяснительной.')
        user['inventory'].append('card')
        transfer_user(user, 'room105')
    elif message == "Просто пойти дальше.":
        bot.send_message(user['id'], 'Куда вы пойдете.', reply_markup=make_default_keyboard())
    else:
        bot.send_message(user['id'], 'Я вас не понял')
