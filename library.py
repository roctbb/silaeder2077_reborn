from config import TOKEN
import telebot
import locations.yard as yard
import locations.gym as gym
import locations.Hall as Hall
import locations.UnderTheCarpet as UnderTheCarpet

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
        "id": "Hall",
        "name": 'холл',
        "inventory": []
    }, 
    {
        "id": "UnderTheCarpet",
        "name": 'комната под ковром',
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
    'Hall': Hall, 
    'UnderTheCarpet': UnderTheCarpet
}
