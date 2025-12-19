from telebot import types
import os

FLAGS = {
    "Web 1": "s2077r{y0u_f0und_m3_1n_D0M}",
    "XSS 1": "s2077r{x33_se@rch}"
}
curr_tasks = {}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for task in FLAGS.keys():
        keyboard.add(types.KeyboardButton(f"{task}{' (Решено)' if f'ctf_{task}' in user['tasks_done'] else ''}"))
    keyboard.add(types.KeyboardButton("Переход: холл 2 этажа"))
    bot.send_message(user["id"], "Вы зашли на кружок по CTF\nВыберите задание:", reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user["id"], "Вы покинули каб. CTF")


def user_message(bot, message, user, location, all_users):
    if message.endswith(" (Решено)") and message[:-9] in FLAGS.keys():
        message = message[:-9]
    if message in FLAGS.keys():
        if f'ctf_{message}' in user["tasks_done"]:
            bot.send_message(user["id"], "Вы уже решили это задание")
            return
        if user["energy"] < 2:
            bot.send_message(user["id"], "У вас недостаточно энергии")
            return
        curr_tasks[user["id"]] = message
        dirname = os.path.split(os.path.split(__file__)[0])[0]
        filename = os.path.join(dirname, f"assets/web/{message.lower().replace(' ', '')}.html")
        bot.send_document(user["id"], types.InputFile(filename), caption=f"Пришлите флаг к заданию \"{message}\" "
                                                                         "(формат s2077r{})")
    elif message in FLAGS.values() and user["id"] in curr_tasks and FLAGS[curr_tasks[user["id"]]] == message:
        if f'ctf_{curr_tasks[user["id"]]}' in user["tasks_done"]:
            bot.send_message(user["id"], "Вы уже решили это задание")
            return
        user["experience"] += 2
        user["tasks_done"].append(f'ctf_{curr_tasks[user["id"]]}')
        curr_tasks.pop(user["id"])
        bot.send_message(user["id"], "Правильный флаг!\nВы получили 2 единицы опыта")
    elif user["id"] in curr_tasks and message.startswith("s2077r{") and message.endswith("}"):
        if f'ctf_{curr_tasks[user["id"]]}' in user["tasks_done"]:
            bot.send_message(user["id"], "Вы уже решили это задание")
            return
        user["energy"] = max(0, user["energy"] - 2)
        bot.send_message(user["id"], f"Неправильный флаг!\nУ вас теперь {user['energy']} энергии")
    else:
        bot.send_message(user["id"], "Я вас не понял")
