from telebot import types
from library import *
import random
from datetime import datetime

def send_welcome(user):
    bot.send_message(user['id'], 'Добро пожаловать в игру!')


def getLocList():
    keys = []
    for i in locations:
        keys.append(i['id'])
    return keys


def get_user(message):
    for user in users:
        if user['id'] == str(message.chat.id):
            return user
    return None


def create_keyboard(buttons, rowsWidth=3):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=rowsWidth)

    for button in buttons:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard


# methods.py (дополняем функцию register_user)

# В функции register_user добавляем:
def register_user(message):
    new_user = {
        'id': str(message.chat.id),
        'name': message.chat.first_name,
        'inventory': [],
        'location': None,
        'energy': 100,
        'food': 100,
        'water': 100,
        'experience': 0,
        'dop_HP': 0,
        'оружие': 0,
        'ochota': 1,
        'obiyasnitelinee': 0,
        'obiyasnitelnay': [],
        'HP': 100,
        'silаedry': 0,
        'unconscious_until': None,
        'last_activity': datetime.now().isoformat(),
        'last_explanation_time': None,  # Время последней объяснительной
        'hall_exits_count': 0,  # Счетчик выходов из холла во время уроков
        'hall_exits_reset_time': None,  # Время сброса счетчика
        'tasks_done': [],
    }

    users.append(new_user)
    return new_user


def get_location_by_id(location_id):
    for location in locations:
        if location['id'] == location_id:
            return location
    return None

def get_location_by_name(location_name):
    for location in locations:
        if location['name'] == location_name:
            return location
    return None


def get_location_users(location_id):
    return list(filter(lambda user: user['location'] == location_id, users))


def get_locations_list():
    keys = []
    for i in locations:
        keys.append(i['id'])
    return keys
def force_explanation(user, reason="нарушение правил"):
    """Принудительно отправляет игрока писать объяснительную"""
    user['ochota'] = 3  # Принудительная объяснительная
    user['explanation_reason'] = reason
    transfer_user_with_goal(user, 'room105', 'force')
    return f"Вы отправлены в 105 за {reason}!"


def transfer_user(user, to_location_id):
    # ДОБАВЬТЕ ЭТОТ КОД В НАЧАЛО ФУНКЦИИ:
    # Автоматически преобразуем старые названия локаций
    location_aliases = {
        'hall': 'hall_1',
        'hall1': 'hall_1',
        'hall2': 'hall_2',
        'hall4': 'hall_4',
        'toilet': 'toilet_1',
    }

    if to_location_id in location_aliases:
        to_location_id = location_aliases[to_location_id]

    from_location_id = user['location']
    new_location = get_location_by_id(to_location_id)

    if random.randint(1, 20) == 1:
        new_location = get_location_by_id('UnderTheCarpet')
        to_location_id = 'UnderTheCarpet'

    user['location'] = to_location_id

    if from_location_id:
        old_location = get_location_by_id(from_location_id)
        modules[from_location_id].user_leaves_location(bot, user, old_location, get_location_users(from_location_id))

    modules[to_location_id].user_enters_location(bot, user, new_location, get_location_users(to_location_id))

# В methods.py добавляем:

def transfer_silaedry(bot, from_user, to_user_id, amount):
    """Перевод Силаэдров между игроками"""
    # Находим получателя
    to_user = None
    for user in users:
        if user['id'] == to_user_id:
            to_user = user
            break

    if not to_user:
        return False, "Получатель не найден"

    # Проверяем баланс
    from_balance = from_user.get('silаedry', 0)
    if from_balance < amount:
        return False, "Недостаточно Силаэдров"

    if amount <= 0:
        return False, "Неверная сумма"

    # Выполняем перевод
    from_user['silаedry'] = from_balance - amount
    to_user['silаedry'] = to_user.get('silаedry', 0) + amount

    # Уведомляем игроков
    bot.send_message(from_user['id'], f"✅ Вы перевели {amount} Силаэдров игроку {to_user['name']}")
    bot.send_message(to_user_id, f"💸 Вы получили {amount} Силаэдров от игрока {from_user['name']}")

    return True, "Перевод выполнен"