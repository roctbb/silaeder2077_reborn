from config import TOKEN
import telebot

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


bot = telebot.TeleBot(TOKEN)
