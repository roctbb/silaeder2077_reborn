from telebot import types
import random


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть"))
    keyboard.add(types.KeyboardButton(text="Поиграть в футбол"))
    keyboard.add(types.KeyboardButton(text="Переход: двор"))
    keyboard.add(types.KeyboardButton(text="Переход: холл"))
    bot.send_message(user['id'], 'Вы на заднем дворе', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули задний двор')


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть':
        user['energy'] = min(100, user['energy'] + 5)
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'])
        if user['energy'] <= 0:
            bot.send_message(user['id'], "у вас слишком мало энергии")
        else:
            with open('assets/images/отдых.png', 'rb') as photo:
                bot.send_photo(user['id'], photo)
            bot.send_message(user['id'], f'Вы отдохнули \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    elif message == 'Поиграть в футбол':
        user['energy'] = min(100, user['energy'] - 5)
        if user['energy'] <= 0:
            bot.send_message(user['id'], "у вас слишком мало энергии")
        else:
            with open('assets/images/response.jpg', 'rb') as photo:
                bot.send_photo(user['id'], photo)
            bot.send_message(user['id'], f'Вы поиграли в футбол\n'
                                     f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')
            bot.send_message(user['id'], f"Вы заметили что на улице никого нет")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Пнуть мяч в окно"))
            keyboard.add(types.KeyboardButton(text="ничего не делать"))
            keyboard.add(types.KeyboardButton(text="Отжиматься"))
            keyboard.add(types.KeyboardButton(text="Переход: двор"))
            keyboard.add(types.KeyboardButton(text="Переход: холл"))
            bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)
    elif message == "Пнуть мяч в окно":
        with open('assets/images/мяч_окно.png', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        bot.send_message(user['id'], "Что у вас за мысли?\nВ 105!")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Переход: каб. 105"))
        bot.send_message(user['id'], f'Переход: каб. 105', reply_markup=keyboard)
    elif message == "Отжиматься":
        with open('assets/images/img.png', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        user['experience'] = min(100, user['experience'] + 1)
        user['energy'] = min(100, user['energy'] - 5)
        bot.send_message(user['id'], "Ок. Вы хороший ученик. Вас не отправят в 105 :)")
        bot.send_message(user['id'], f'Вы отжались \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    elif message == "ничего не делать":
        user['energy'] = min(100, user['energy'] + 5)
        with open('assets/images/бездействие    .png', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        bot.send_message(user['id'], f'Вы отдохнули \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')
    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
