from config import TOKEN
import telebot
import locations.yard as yard
import locations.gym as gym
import locations.UnderTheCarpet as UnderTheCarpet
import locations.hall as hall
import locations.room_116 as room_116
bot = telebot.TeleBot(TOKEN)

users = []

locations = [
    {
        "id": "yard",
        "name": 'двор',
        "inventory": []
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
        "id": "room_116",
        "name": 'каб. 116',
        "inventory": []
    }
]

def getLocList():
    keys = []
    for i in locations:
        keys.append(i['id'])
    return keys

modules = {
    'yard': yard,
    'gym': gym,
    'UnderTheCarpet': UnderTheCarpet, 
    'hall': hall,
    'room_116' : room_116
}
