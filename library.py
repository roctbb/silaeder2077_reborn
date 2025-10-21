from config import TOKEN
import telebot
import locations.yard as yard
import locations.gym as gym
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
        "id": "room_116",
        "name": 'каб. 116',
        "inventory": []
    }
]

modules = {
    'yard': yard,
    'gym': gym,
    'hall': hall,
    'room_116' : room_116
}
