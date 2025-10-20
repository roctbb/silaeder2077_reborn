from config import TOKEN
import telebot
import locations.yard as yard

bot = telebot.TeleBot(TOKEN)

users = []

locations = [
    {
        "id": "yard",
        "name": 'двор',
        "inventory": [],
    },
    {
        "id": "116",
        "name": 'каб. 116',
        "inventory": []
             }
]

modules = {
    'yard': yard
}
