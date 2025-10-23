from telebot import types
import random

tasks = {
    "Велосипедист проехал 36 км за 2 часа. Найдите среднюю скорость велосипедиста.": 18,
    "Автомобиль движется со скоростью 60 км/ч. Какое расстояние он преодолеет за 45 минут?": 45,
    "Пешеход прошёл 6 км со скоростью 5 км/ч. Сколько времени занял путь?": 1.2
}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поговорить с Алексеем Генадьевичем"))
    keyboard.add(types.KeyboardButton(text="Посмотреть на мусор(может это не мусор, я не знаю) в коробке"))
    keyboard.add(types.KeyboardButton(text="Попросить конфетку"))
    bot.send_message(user['id'], 'Вы в каб. Физики', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. Физики')


def user_message(bot, message, user, location, all_users):
    if message == 'Поговорить с Алексеем Генадьевичем':
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'] + 1)
        else:
            bot.send_message(user['id'], f'Дастиш вери гуд, что ты пришел. А теперь атеншен на доску. У вас будет не сколько задачек.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)#
            keyboard.add(types.KeyboardButton(text="1"))
            keyboard.add(types.KeyboardButton(text="2"))
            keyboard.add(types.KeyboardButton(text="3"))
            bot.send_message(user['id'], 'Какую выберете задачу?', reply_markup=keyboard)
    elif message == 'Посмотреть на мусор(может это не мусор, я не знаю) в коробке':
        user['energy'] -= 5
        bot.send_message(user['id'], f'Вы порылись в коробке и нашли несколько интересных вещей\n'
                                 f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')
        bot.send_message(user['id'], f"Вы заметили что на ноутбуке рядом открыт дневник. Можно изменить себе оценки")
        if random.randint(0, 3) == 1:
            bot.send_message(user['id'], f'Вас спалил учитель!!!'
                                         f'И отвели в 105...')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Изменить оценки"))
        keyboard.add(types.KeyboardButton(text="Не менять оценки"))
        keyboard.add(types.KeyboardButton(text="Перейти во холл"))
        bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)



                #bot.send_message(user['id'], f'Перейти в каб. 105')
    elif message == "Изменить оценки":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Перейти в каб. 105"))
        bot.send_message(user['id'], 'Что у вас за мысли?\nВ 105!!!!!!', reply_markup=keyboard)
    elif message == "Не менять оценки":
        bot.send_message(user['id'], "Ок. Вы хороший ученик. Вас не отправят в 105 :)")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Поиграть на пианино"))
        keyboard.add(types.KeyboardButton(text="Потыкать по доске"))
        keyboard.add(types.KeyboardButton(text="Перейти во холл"))
        bot.send_message(user['id'], 'Вы в каб. 116', reply_markup=keyboard)


    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
