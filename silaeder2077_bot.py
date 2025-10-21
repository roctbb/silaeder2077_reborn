import telebot
from library import *
from methods import *
from telebot import types
from config import TOKEN

@bot.message_handler(content_types=['text'])
def process_text(message):
    user = get_user(message)
    print(user)

    if not user:
        user = register_user(message)
        send_welcome(user)
        transfer_user(user, 'yard')

    else:
        message_text = message.text

        if message_text.startswith('Перейти в '):
            location = get_location_by_name(message_text.replace('Перейти в ', ''))
            transfer_user(user, location['id'])
        else:
            location = get_location_by_id(user['location'])
            neighbours = get_location_users(user['location'])
            modules[user['location']].user_message(bot, message_text, user, location, neighbours)


bot.polling(none_stop=True)
