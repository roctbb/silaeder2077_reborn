from config import TOKEN
import telebot
import json

modules = {}
users = []

locations = [
    {
        "id": "yard",
        "name": 'двор',
    },
    {
        "id": "gym",
        "name": 'спортзал',
        "inventory": []
    },
    {
        "id": "hall",
        "name": 'холл',
        "inventory": []
    },
    {
        "id": "UnderTheCarpet",
        "name": 'комната под ковром',
    },
    {
        "id": "room116",
        "name": 'каб. 116',
        "inventory": []
    },
    {
        "id": "room105",
        "name": 'каб. 105',
        "inventory": []
    },
    {
        "id": "toilet",
        "name": 'туалет',
        "inventory": []
    },
    {
        "id": "dining_room",
        "name": 'столовая',
        "inventory": []
    },
    {
        "id": "back_yard",
        "name": 'задний двор',
        "inventory": []
    },
    {
        "id": "math",
        "name": 'каб. Математики',
        "inventory": []
    },
    {
        "id": "room_physics",
        "name": 'каб. Физики',
        "inventory": []
    },
    {
        "id": "home",
        "name": 'дом',
        "inventory": []
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
        })

        file.write(state)


def load_modules():
    import locations.yard as yard
    import locations.gym as gym
    import locations.UnderTheCarpet as UnderTheCarpet
    import locations.hall as hall
    import locations.room116 as room116
    import locations.room105 as room105
    import locations.dining_room as dining_room
    import locations.toilet as toilet
    import locations.math as math
    import locations.room_physics as room_physics
    import locations.back_yard as back_yard
    import locations.home as home

    modules.update({
        'yard': yard,
        'gym': gym,
        'UnderTheCarpet': UnderTheCarpet,
        'hall': hall,
        'room116': room116,
        'room105': room105,
        'dining_room': dining_room,
        'toilet': toilet,
        'back_yard': back_yard,
        'math': math,
        'room_physics': room_physics,
        'home': home
    })


def load_state():
    try:
        saved_users, saved_locations = load_state_from_file()
        users.extend(saved_users)
        locations.clear()
        locations.extend(saved_locations)
        print("Loaded state from file: ", users, locations)

    except Exception as e:
        print(e)


bot = telebot.TeleBot(TOKEN)
