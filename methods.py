from telebot import types
from library import *
import random

def send_welcome(user):
    bot.send_message(user['id'], 'Добро пожаловать в игру!')


def getLocList():
    keys = []
    for i in locations:
        keys.append(i['id'])
    return keys


def get_user(message):
    for user in users:
        if user['id'] == message.chat.id:
            return user
    return None


def create_keyboard(buttons, rowsWidth=3):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=rowsWidth)

    for button in buttons:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard


def register_user(message):
    new_user = {
        'id': message.chat.id,
        'name': message.chat.first_name,
        'inventory': [],
        'location': None,
        'energy': 100,
        'food': 100,
        'water': 100,
        'experience': 0,
        'dop_HP': 0,
        'оружие': 0
    }

    users.append(new_user)

    return new_user


def get_location_by_id(location_id):
    for location in locations:
        if location['id'] == location_id:
            return location
    return None


def get_location_by_name(location_name):
    for location in locations:
        if location['name'] == location_name:
            return location
    return None


def get_location_users(location_id):
    return list(filter(lambda user: user['location'] == location_id, users))


def get_locations_list():
    keys = []
    for i in locations:
        keys.append(i['id'])
    return keys


def transfer_user(user, to_location_id):
    from_location_id = user['location']
    new_location = get_location_by_id(to_location_id)
    if random.randint(1, 10) == 1:
        new_location = get_location_by_id('UnderTheCarpet')
        to_location_id = 'UnderTheCarpet'
    user['location'] = to_location_id

    if from_location_id:
        old_location = get_location_by_id(from_location_id)
        modules[from_location_id].user_leaves_location(bot, user, old_location, get_location_users(from_location_id))

    modules[to_location_id].user_enters_location(bot, user, new_location, get_location_users(to_location_id))
