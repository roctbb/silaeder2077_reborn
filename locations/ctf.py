from telebot import types
import os

FLAGS = {
    "Web 1": "s2077r{y0u_f0und_m3}"
}
curr_tasks = {}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Попросить у Ильи задания"))
    keyboard.add(types.KeyboardButton("Переход: холл 2 этажа"))
    bot.send_message(user["id"], "Вы зашли на кружок по CTF", reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user["id"], "Вы покинули каб. CTF")


def user_message(bot, message, user, location, all_users):
    if message == "Попросить у Ильи задания":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for task in FLAGS.keys():
            keyboard.add(types.KeyboardButton(task))
        keyboard.add(types.KeyboardButton("Переход: холл 2 этажа"))
        bot.send_message(user["id"], "Выбери задание:", reply_markup=keyboard)
    elif message in FLAGS.keys():
        curr_tasks[user["id"]] = message
        dirname = os.path.split(os.path.split(__file__)[0])[0]
        filename = os.path.join(dirname, f"assets/web/{message.lower().replace(" ", "")}.html")
        bot.send_document(user["id"], types.InputFile(filename), caption=f"Пришлите флаг к заданию \"{message}\"")
    elif message in FLAGS.values() and user["id"] in curr_tasks and FLAGS[curr_tasks[user["id"]]] == message:
        user["experience"] = min(100, user["experience"] + 2)
        curr_tasks.pop(user["id"])
        bot.send_message(user["id"], "Правильный флаг!\nВы получили 2 единицы опыта")
    elif user["id"] in curr_tasks:
        user["energy"] = max(0, user["energy"] - 2)
        bot.send_message(user["id"], f"Неправильный флаг!\nУ вас теперь {user['energy']} энергии")
    else:
        bot.send_message(user["id"], "Я вас не понял")
