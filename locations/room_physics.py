from telebot import types
from methods import send_photo
import random

num_task = {}

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
    keyboard.add(types.KeyboardButton(text="Переход: холл 4 этажа"))
    send_photo(bot, user['id'], 'assets/images/физика.jpg', 'Вы в каб. Физики', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. Физики')


def user_message(bot, message, user, location, all_users):
    global num_task, tasks

    if message == 'Поговорить с Алексеем Генадьевичем':
        if random.randint(1, 10) == 1:
            user['experience'] += 1
            bot.send_message(user['id'], 'Вы получили 1 единицу опыта!')
        else:
            bot.send_message(user['id'],
                             'Дастиш вери гуд, что ты пришел. А теперь атеншен на доску. У вас будет несколько задачек.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text=f"1{' (Решено)' if 'phys_1' in user['tasks_done'] else ''}"))
            keyboard.add(types.KeyboardButton(text=f"2{' (Решено)' if 'phys_2' in user['tasks_done'] else ''}"))
            keyboard.add(types.KeyboardButton(text=f"3{' (Решено)' if 'phys_3' in user['tasks_done'] else ''}"))
            keyboard.add(types.KeyboardButton(text="Переход: холл 4 этажа"))
            bot.send_message(user['id'], 'Какую выберете задачу?', reply_markup=keyboard)

    elif message == 'Посмотреть на мусор(может это не мусор, я не знаю) в коробке':
        user['energy'] -= 5
        send_photo(bot, user['id'], 'assets/images/коробка.jpg',
                   f'Вы порылись в коробке и нашли несколько интересных вещей\n'
                   f'У вас теперь {user["energy"]} энергии, но у вас поднялось настроение')

    elif message == "Попросить конфетку":
        bot.send_message(user['id'], '0о\n -')

    elif message in ("1", "1 (Решено)", "2", "2 (Решено)", "3", "3 (Решено)"):
        if message.endswith(" (Решено)"):
            message = message[:-9]
        if f"phys_{message}" in user["tasks_done"]:
            bot.send_message(user["id"], "Вы уже решили это задание")
            return
        num_task[user["id"]] = int(message)
        task_text = list(tasks.keys())[num_task[user["id"]] - 1]
        bot.send_message(user['id'], task_text)
        bot.send_message(user['id'], "Напишите ответ на задачу\nПишите нецелые числа через точку")

    elif num_task[user["id"]] != 0:
        if f"phys_{num_task[user["id"]]}" in user["tasks_done"]:
            bot.send_message(user["id"], "Вы уже решили это задание")
            return
        correct_answer = list(tasks.values())[num_task[user["id"]] - 1]

        try:
            user_answer = float(message)
            if abs(user_answer - correct_answer) < 0.01:
                bot.send_message(user['id'], "Дастиш вери гуд!!!")
                user['experience'] += 5
                user["tasks_done"].append(f"phys_{num_task[user["id"]]}")
                num_task[user["id"]] = 0
            else:
                bot.send_message(user['id'], "Оууу, оууу. Это фигня какая-то")
                num_task[user["id"]] = 0
        except ValueError:
            bot.send_message(user['id'], "Пожалуйста, введите число в правильном формате")

    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')
