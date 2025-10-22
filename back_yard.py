from telebot import types
import random


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть"))
    keyboard.add(types.KeyboardButton(text="Поиграть в футбол"))
    keyboard.add(types.KeyboardButton(text="Перейти в спортзал"))
    bot.send_message(user['id'], 'Вы на заднем дворе Мирона', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули задний двор Мирона')


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть':
        user['energy'] = min(100, user['energy'] + 5)
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'])
        if user['energy'] <= 0:
            bot.send_message(user['id'], "ВЫ УМЕРЛИ!!!")
        else:
            bot.send_message(user['id'], f'Вы отдохнули \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    elif message == 'Поиграть в футбол':
        user['energy'] = min(100, user['energy'] - 5)
        if user['energy'] <= 0:
            bot.send_message(user['id'], "ВЫ УМЕРЛИ!!!")
        else:
            bot.send_message(user['id'], f'Вы поиграли в футбод\n'
                                     f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')
            bot.send_message(user['id'], f"Вы заметили что на улице никого нет")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Пнуть мяч в окно"))
            keyboard.add(types.KeyboardButton(text="ничего не делать"))
            keyboard.add(types.KeyboardButton(text="Отжиматься"))
            bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)
            if random.randint(0, 3) == 1:
                bot.send_message(user['id'], f'Вас спалил учитель!!!'
                                             f'И отвели в 105...')
                bot.send_message(user['id'], f'Перейти в каб. 105')
    elif message == "Пнуть мяч в окно":
        bot.send_message(user['id'], "Что у вас за мысли?\nВ 105!!!!!!")

        bot.send_message(user['id'], f'Перейти в каб. 105')
    elif message == "Отжиматься":
        bot.send_message(user['id'], "Ок. Вы хороший ученик. Вас не отправят в 105 :)")


    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
