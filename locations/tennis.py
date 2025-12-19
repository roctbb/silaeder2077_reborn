from telebot import types
import random

points = {}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Загасить"))
    keyboard.add(types.KeyboardButton("Просто отбить"))
    keyboard.add(types.KeyboardButton("Переход: холл 2 этажа"))
    points[user["id"]] = [0, 0]
    bot.send_message(user["id"], "Вы подошли к теннисному столу\nСоперник уже ждёт вас\nЧто вы будете делать?",
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user["id"], "Вы покинули теннисный стол")


def user_message(bot, message, user, location, all_users):
    if message == "Загасить":
        if user["energy"] < 2:
            bot.send_message(user["id"], "У вас недостаточно энергии")
            return
        user["energy"] -= 2
        if random.randint(1, 2) == 1:
            if random.randint(1, 3) == 1:
                bot.send_message(user["id"],
                                 f"Вы гасите по своему сопернику, но он мяч отбивает\nУ вас {user['energy']} энегрии")
            else:
                points[user["id"]][0] += 1
                bot.send_message(user["id"],
                                 f"Вы гасите по своему сопернику, он мяч не отбивает\n"
                                 f"Счёт {points[user["id"]][0]}-{points[user["id"]][1]}\n"
                                 f"У вас {user['energy']} энегрии")
        else:
            if random.randint(1, 3) == 1:
                bot.send_message(user["id"], f"Вы пытаетесь загасить по своему сопернику, но промахнулись\n"
                                             f"Он гасит в вас, но вы отбиваете\n"
                                             f"Счёт {points[user["id"]][0]}-{points[user["id"]][1]}\n"
                                             f"У вас {user['energy']} энегрии")
            else:
                points[user["id"]][1] += 1
                bot.send_message(user["id"], f"Вы пытаетесь загасить по своему сопернику, но промахнулись\n"
                                             f"Он гасит в вас, и вы не отбиваете\n"
                                             f"Счёт {points[user["id"]][0]}-{points[user["id"]][1]}\n"
                                             f"У вас {user['energy']} энегрии")
    else:
        bot.send_message(user["id"], "Я вас не понял")
