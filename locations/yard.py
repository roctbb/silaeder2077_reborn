from telebot import types
import random
from datetime import datetime
from methods import *  # Добавляем импорт методов


def is_winter_season():
    """Проверяет, сейчас зима или нет"""
    now = datetime.now()
    month = now.month

    # Зима: декабрь, январь, февраль
    return month in [12, 1, 2]


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть на лавочке"))
    keyboard.add(types.KeyboardButton(text="Переход: задний двор"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    keyboard.add(types.KeyboardButton(text="Переход: дом"))

    # Если зима и есть другие игроки, добавляем кнопку снежков
    if is_winter_season() and len(all_users) > 1:
        keyboard.add(types.KeyboardButton(text="❄️ Кидаться снежками"))

    send_photo(bot, user['id'], "assets/images/yard.jpg", 'Вы во дворе', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете двор')


def throw_snowballs(bot, user, all_users):
    """Обработка кидания снежками"""
    # Находим других игроков в локации
    other_users = [u for u in all_users if u['id'] != user['id']]

    if not other_users:
        bot.send_message(user['id'], 'Не с кем кидаться снежками!')
        return

    # Выбираем случайную цель
    target = random.choice(other_users)

    # Определяем результат
    results = [
        f"Вы слепили огромный снежок и попали в {target['name']}! ☃️",
        f"Снежок развалился в воздухе, не долетев до {target['name']}...",
        f"Вы попали снежком в {target['name']} со всей силы! ❄️💥",
        f"{target['name']} поймал ваш снежок и кинул обратно!"
    ]

    result = random.choice(results)

    # Расход энергии
    user['energy'] = max(0, user.get('energy', 100) - 5)

    # Отправляем результат
    bot.send_message(user['id'],
                     f"{result}\nВы потратили 5% энергии. Осталось: {user['energy']}%")

    # Уведомляем цель (шанс 33%)
    if random.randint(1, 3) == 1:
        responses = [
            f"{user['name']} закидал вас снежками! ❄️",
            f"Вас атаковали снежками от {user['name']}!",
            f"Снежная битва с {user['name']} началась!"
        ]
        bot.send_message(target['id'], random.choice(responses))


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть на лавочке':
        user['energy'] = min(100, user.get('energy', 100) + 5)
        bot.send_message(user['id'], f'Вы передохнули на лавочке пару минут. Теперь у вас {user["energy"]}% энергии.')

    elif message == 'Переход: задний двор':
        transfer_user(user, 'back_yard')

    elif message == 'Переход: холл 1 этажа':
        transfer_user(user, 'hall_1')

    elif message == '❄️ Кидаться снежками':
        if is_winter_season():
            throw_snowballs(bot, user, all_users)
        else:
            bot.send_message(user['id'], 'Сейчас не зима, снежков нет!')
    else:
        bot.send_message(user['id'], 'Я вас не понял')
