from config import TOKEN
import telebot
import json
from datetime import datetime
modules = {}
users = []

# library.py - обновляем список locations
locations = [
    {
        "id": "yard",
        "name": 'двор',
        "locations": ["задний двор", "холл 1 этажа", "дом"],
    },
    {
        "id": "gym",
        "name": 'спортзал',
        "inventory": [],
        "locations": ["холл 1 этажа", "спортзал"],
    },
    {
        "id": "hall_1",
        "name": 'холл 1 этажа',
        "inventory": [],
        "locations": ["лестница с 1 на 2 этаж", "каб. 105", "каб. 116", "комната охраны", "двор", "задний двор",
                      "столовая", "спортзал"],
    },
    {
        "id": "hall_2",
        "name": 'холл 2 этажа',
        "inventory": [],
        "locations": ["туалет 2 этажа", "каб. Математики", "каб. CTF", "теннисный стол", "лестница с 1 на 2 этаж",
                      "лестница со 2 на 4 этаж"],
    },
    {
        "id": "hall_4",
        "name": 'холл 4 этажа',
        "inventory": [],
        "locations": ["каб. Физики", "лестница со 2 на 4 этаж"],
    },
    {
        "id": "stairs_1_2",
        "name": 'лестница с 1 на 2 этаж',
        "locations": ["холл 1 этажа", "холл 2 этажа"],
    },
    {
        "id": "stairs_2_4",
        "name": 'лестница со 2 на 4 этаж',
        "locations": ["холл 2 этажа", "холл 4 этажа"],
    },
    {
        "id": "UnderTheCarpet",
        "name": 'комната под ковром',
        "inventory": [], 
        "data": {},
        "locations": [],
    },
    {
        "id": "room116",
        "name": 'каб. 116',
        "inventory": [],
        "locations": ["холл 1 этажа", "каб. 105"],
    },
    {
        "id": "room105",
        "name": 'каб. 105',
        "inventory": [],
        "locations": [],
    },
    {
        "id": "toilet_1",
        "name": 'туалет 1 этажа',
        "inventory": [],
        "locations": ["холл 1 этажа"],
    },
    {
        "id": "toilet_2",
        "name": 'туалет 2 этажа',
        "inventory": [],
        "locations": ["холл 2 этажа"],
    },
    {
        "id": "dining_room",
        "name": 'столовая',
        "inventory": [],
        "locations": ["холл 1 этажа", "каб. 105"],
    },
    {
        "id": "back_yard",
        "name": 'задний двор',
        "inventory": [],
        "locations": ["двор", "холл 1 этажа"],
    },
    {
        "id": "math",
        "name": 'каб. Математики',
        "inventory": [],
        "locations": ["холл 2 этажа"],
    },
    {
        "id": "room_physics",
        "name": 'каб. Физики',
        "inventory": [],
        "locations": ["холл 4 этажа"],
    },
    {
        "id": "home",
        "name": 'дом',
        "inventory": [],
        "locations": [],
    },
    {
        "id": "security",
        "name": 'комната охраны',
        "inventory": [],
        "locations": ["холл 1 этажа"],
    },
    {
        "id": "CTF",
        "name": "каб. CTF",
        "locations": ["холл 2 этажа"],
    },
    {
        "id": "tennis",
        "name": "теннисный стол",
        "locations": ["холл 2 этажа"],
    }
]


def load_state_from_file():
    with open('state.json', 'r', encoding='utf-8') as file:
        data = file.read()
        state = json.loads(data)

    return state['users'], state['locations']


def save_state_to_file(users, locations):
    with open('state.json', 'w', encoding='utf-8') as file:
        state = json.dumps({
            'users': users,
            'locations': locations
        }, ensure_ascii=False, indent=4, separators=(',', ':'))

        file.write(state)


def load_modules():
    import locations.yard as yard
    import locations.gym as gym
    import locations.UnderTheCarpet as UnderTheCarpet
    import locations.hall_1 as hall_1
    import locations.hall_2 as hall_2
    import locations.hall_4 as hall_4
    import locations.stairs_1_2 as stairs_1_2
    import locations.stairs_2_4 as stairs_2_4
    import locations.room116 as room116
    import locations.room105 as room105
    import locations.dining_room as dining_room
    import locations.toilet_1 as toilet_1
    import locations.toilet_2 as toilet_2
    import locations.back_yard as back_yard
    import locations.math as math
    import locations.room_physics as room_physics
    import locations.home as home
    import locations.security as security
    import locations.ctf as ctf
    import locations.tennis as tennis

    modules.update({
        'yard': yard,
        'gym': gym,
        'UnderTheCarpet': UnderTheCarpet,
        'hall': hall_1,  # АЛИАС ДЛЯ СТАРОГО КОДА
        'hall_1': hall_1,
        'hall_2': hall_2,
        'hall_4': hall_4,
        'stairs_1_2': stairs_1_2,
        'stairs_2_4': stairs_2_4,
        'room116': room116,
        'room105': room105,
        'dining_room': dining_room,
        'toilet_1': toilet_1,
        'toilet_2': toilet_2,
        'back_yard': back_yard,
        'math': math,
        'room_physics': room_physics,
        'home': home,
        'security': security,
        'CTF': ctf,
        'tennis': tennis
    })
def load_state():
    try:
        saved_users, saved_locations = load_state_from_file()

        # Обновляем пользователей, добавляя недостающие поля
        for user in saved_users:
            # Добавляем новые поля если их нет
            if 'HP' not in user:
                user['HP'] = 100
            if 'silаedry' not in user:
                user['silаedry'] = 0
            if 'unconscious_until' not in user:
                user['unconscious_until'] = None
            if 'last_activity' not in user:
                user['last_activity'] = datetime.now().isoformat()
            if 'ochota' not in user:
                user['ochota'] = 1
            if 'obiyasnitelinee' not in user:
                user['obiyasnitelinee'] = 0
            if 'obiyasnitelnay' not in user:
                user['obiyasnitelnay'] = []

        users.extend(saved_users)
        locations.clear()
        locations.extend(saved_locations)
        print("Loaded state from file")

    except Exception as e:
        print(e)


bot = telebot.TeleBot(TOKEN)
