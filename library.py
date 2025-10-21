from config import TOKEN
import telebot
import locations.yard as yard
import locations.gym as gym

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
    }
]

modules = {
    'yard': yard,
    'gym': gym,
    'Hall': Hall
}
