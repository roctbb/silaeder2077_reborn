from telebot import types
import random
from datetime import datetime


def is_winter_season():
    """Проверяет, сейчас зима или нет"""
    now = datetime.now()
    month = now.month
    return month in [12, 1, 2]


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть"))
    keyboard.add(types.KeyboardButton(text="Поиграть в футбол"))
    keyboard.add(types.KeyboardButton(text="Переход: двор"))
    keyboard.add(types.KeyboardButton(text="Переход: холл"))

    # Если зима и есть другие игроки, добавляем кнопку снежков
    if is_winter_season() and len(all_users) > 1:
        keyboard.add(types.KeyboardButton(text="❄️ Кидаться снежками"))

    bot.send_message(user['id'], 'Вы на заднем дворе', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули задний двор')


def throw_snowballs(bot, user, all_users):
    """Обработка кидания снежками"""
    other_users = [u for u in all_users if u['id'] != user['id']]

    if not other_users:
        bot.send_message(user['id'], 'Не с кем кидаться снежками!')
        return

    target = random.choice(other_users)

    results = [
        f"Вы слепили огромный снежок и попали в {target['name']}! ☃️",
        f"Снежок развалился в воздухе, не долетев до {target['name']}...",
        f"Вы попали снежком в {target['name']} со всей силы! ❄️💥",
        f"{target['name']} поймал ваш снежок и кинул обратно!"
    ]

    result = random.choice(results)

    user['energy'] = max(0, user.get('energy', 100) - 5)

    bot.send_message(user['id'],
                     f"{result}\nВы потратили 5% энергии. Осталось: {user['energy']}%")

    if random.randint(1, 3) == 1:
        responses = [
            f"{user['name']} закидал вас снежками на заднем дворе! ❄️",
            f"Вас атаковали снежками от {user['name']}!",
            f"Снежная битва с {user['name']} началась!"
        ]
        bot.send_message(target['id'], random.choice(responses))


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть':
        user['energy'] = min(100, user['energy'] + 5)
        if random.randint(1, 10) == 1:
            user['experience'] = min(100, user['experience'])
        else:
            bot.send_message(user['id'],
                             f'Вы отдохнули \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')

    elif message == 'Поиграть в футбол':
        user['energy'] = min(100, user['energy'] - 5)
        if user['energy'] <= 0:
            bot.send_message(user['id'], "у вас слишком мало энергии")
        else:
            bot.send_message(user['id'],
                             f'Вы поиграли в футбол\nУ вас теперь {user["energy"]} энергии, но у вас поднялось настроение')
            bot.send_message(user['id'], f"Вы заметили что на улице никого нет")

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Пнуть мяч в окно"))
            keyboard.add(types.KeyboardButton(text="ничего не делать"))
            keyboard.add(types.KeyboardButton(text="Отжиматься"))
            keyboard.add(types.KeyboardButton(text="Переход: двор"))
            keyboard.add(types.KeyboardButton(text="Переход: холл"))

            # Если зима, добавляем снежки
            if is_winter_season() and len(all_users) > 1:
                keyboard.add(types.KeyboardButton(text="❄️ Кидаться снежками"))

            bot.send_message(user['id'], 'Что будете делать?', reply_markup=keyboard)

    elif message == "Пнуть мяч в окно":
        bot.send_message(user['id'], "Что у вас за мысли?\nВ 105!")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Переход: каб. 105"))
        bot.send_message(user['id'], f'Переход: каб. 105', reply_markup=keyboard)

    elif message == "Отжиматься":
        user['experience'] = min(100, user['experience'] + 1)
        user['energy'] = min(100, user['energy'] - 5)
        bot.send_message(user['id'], "Ок. Вы хороший ученик. Вас не отправят в 105 :)")
        bot.send_message(user['id'],
                         f'Вы отжались \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')

    elif message == "ничего не делать":
        user['energy'] = min(100, user['energy'] + 5)
        bot.send_message(user['id'],
                         f'Вы отдохнули \n Теперь у вас {user["experience"]} опыта и {user["energy"]} энергии')

    elif message == '❄️ Кидаться снежками':
        if is_winter_season():
            throw_snowballs(bot, user, all_users)
        else:
            bot.send_message(user['id'], 'Сейчас не зима, снежков нет!')

    else:
        bot.send_message(user['id'], 'Я вас не понял :(\nНапишите еще раз')