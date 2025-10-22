from telebot import types
import random


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поиграть на пианино"))
    keyboard.add(types.KeyboardButton(text="Потыкать по доске"))
    keyboard.add(types.KeyboardButton(text="Перейти во двор"))
    bot.send_message(user['id'], 'Вы в каб. 116', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. 116')


def user_message(bot, message, user, location, all_users):
    if message == 'Поиграть на пианино':
        user['energy'] = min(100, user['energy'] - 5)
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'] + 1)
        if user['energy'] <= 0:
            bot.send_message(user['id'], "ВЫ УМЕРЛИ!!!")
        else:
            bot.send_message(user['id'], f'Вы поиграли на пианино \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    elif message == 'Потыкать по доске':
        user['energy'] = min(100, user['energy'] - 5)
        if user['energy'] <= 0:
            bot.send_message(user['id'], "ВЫ УМЕРЛИ!!!")
        else:
            bot.send_message(user['id'], f'Вы поиграли на пианино\n'
                                     f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')
            bot.send_message(user['id'], f"Вы заметили что на ноутбуке рядом открыт дневник. Можно изменить себе оценки")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Изменить оценки"))
            keyboard.add(types.KeyboardButton(text="Не менять оценки"))
            bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)


            if random.randint(0, 3) == 1:
                bot.send_message(user['id'], f'Вас спалил учитель!!!'
                                             f'И отвели в 105...')
                #bot.send_message(user['id'], f'Перейти в каб. 105')
    elif message == "Изменить оценки":
        bot.send_message(user['id'], "Что у вас за мысли?")
    elif message == "Не менять оценки":
        bot.send_message(user['id'], "ок")

    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
