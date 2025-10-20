from config import TOKEN
import telebot
import locations.yard as yard

bot = telebot.TeleBot(TOKEN)

users = []

locations = [
    {
        "id": "yard",
        "name": 'двор',
        "inventory": []
    }
]

modules = {
    'yard': yard
}
