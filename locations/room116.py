from telebot import types
from methods import transfer_user, send_photo
import random


def make_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поиграть на пианино"))
    keyboard.add(types.KeyboardButton(text="Потыкать по доске"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    return keyboard


def user_enters_location(bot, user, location, all_users):
    send_photo(bot, user['id'], 'assets/images/116.jpg', 'Вы в каб. 116', reply_markup=make_default_keyboard())



def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. 116')


def user_message(bot, message, user, location, all_users):
    if message == 'Поиграть на пианино':
        user['energy'] = max(0, user['energy'] - 5)
        if random.randint(1, 10) == 1:
            user['experience'] += 1
        send_photo(bot, user['id'], 'assets/images/пианина.jpg',
                   f'Вы поиграли на пианино \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    elif message == 'Потыкать по доске':
        user['energy'] = max(0, user['energy'] - 5)
        send_photo(bot, user['id'], 'assets/images/доска.jpg', f'Вы потыкали по доске\n'
                   f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')

        send_photo(bot, user['id'], 'assets/images/ноут.jpg',
                   f"Вы заметили что на ноутбуке рядом открыт дневник. Можно изменить себе оценки")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Изменить оценки"))
        keyboard.add(types.KeyboardButton(text="Не менять оценки"))
        keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
        bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)
    elif message == "Изменить оценки":
        user["ochota"] = 2
        bot.send_message(user['id'], 'Что у вас за мысли?\nВ 105!!!!!!')
        transfer_user(user, "room105")
    elif message == "Не менять оценки":
        bot.send_message(user['id'], "Ок. Вы хороший ученик. Вас не отправят в 105 :)")
        bot.send_message(user['id'], 'Вы в каб. 116', reply_markup=make_default_keyboard())

    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
