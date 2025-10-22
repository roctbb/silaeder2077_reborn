import telebot
from library import users, locations, bot, modules
from methods import *
from telebot import types
from config import TOKEN

@bot.message_handler(content_types=['text'])
def process_text(message):
    user = get_user(message)


    if not user:
        user = register_user(message)
        send_welcome(user)
        transfer_user(user, 'yard')

    else:

        message_text = message.text

        if message_text.startswith('Перейти в '):
            location = get_location_by_name(message_text.replace('Перейти в ', ''))
            transfer_user(user, location['id'])
        elif message_text.startswith('Перейти во '):
            location = get_location_by_name(message_text.replace('Перейти во ', ''))
            transfer_user(user, location['id'])
            location = get_location_by_id(user['location'])
            neighbours = get_location_users(user['location'])
            try:
                modules[user['location']].user_message(bot, message_text, user, location, neighbours)
            except Exception as e:
                print(e)
    print(user)

bot.polling(none_stop=True)
