from sympy.physics.quantum.qubit import measure_all
from telebot import types
import random

num_task = 0

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
    keyboard.add(types.KeyboardButton(text="Переход: холл"))
    bot.send_message(user['id'], 'Вы в каб. Физики', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. Физики')


def user_message(bot, message, user, location, all_users):
    global num_task, tasks
    if message == 'Поговорить с Алексеем Генадьевичем':
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'] + 1)
        else:
            bot.send_message(user['id'], f'Дастиш вери гуд, что ты пришел. А теперь атеншен на доску. У вас будет несколько задачек.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)#
            keyboard.add(types.KeyboardButton(text="1"))
            keyboard.add(types.KeyboardButton(text="2"))
            keyboard.add(types.KeyboardButton(text="3"))
            keyboard.add(types.KeyboardButton(text="Переход: холл"))
            bot.send_message(user['id'], 'Какую выберете задачу?', reply_markup=keyboard)
    elif message == 'Посмотреть на мусор(может это не мусор, я не знаю) в коробке':
        user['energy'] -= 5
        bot.send_message(user['id'], f'Вы порылись в коробке и нашли несколько интересных вещей\n'
                                 f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')

                #bot.send_message(user['id'], f'Перейти в каб. 105')
    elif message == "Попросить конфетку":
        bot.send_message(user['id'], '0о\n'
                                     ' -')
    elif message == '1' or message == "2" or message == "3":
        num_task = int(message)
        bot.send_message(user['id'], str(list(tasks.items())[num_task-1][0]))
        bot.send_message(user['id'], "Напишите ответ на задачу\nПишите нецелые числа через точку")

    elif num_task != 0:
        if message == tasks[num_task-1]:
            bot.send_message("Дастиш вери гуд!!!")
            user['experience']+=5
        else:
            bot.send_message("Оууу, оууу. Это фигня какая-то")
    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
