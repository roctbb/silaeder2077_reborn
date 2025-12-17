import telebot
from library import users, locations, bot, modules
from methods import *
from telebot import types
from config import TOKEN


@bot.message_handler(content_types=['text'])
def process_text(message):
    user = get_user(message)
    print(message.text, users)
    if not user:
        user = register_user(message)
        send_welcome(user)
        transfer_user(user, 'yard')
    else:
        message_text = message.text
        if message_text.startswith('Переход: '):
            location = get_location_by_name(message_text.replace('Переход: ', ''))
            if location:
                transfer_user(user, location['id'])
            else:
                bot.send_message(user['id'], 'Локация не найдена.')
        else:
            location = get_location_by_id(user['location'])
            neighbours = get_location_users(user['location'])
            try:
                modules[user['location']].user_message(bot, message_text, user, location, neighbours)
            except Exception as e:
                print(e)
    print(users)
    save_state_to_file(users, locations)


if __name__ == '__main__':
    load_modules()
    load_state()
    bot.polling(none_stop=True)