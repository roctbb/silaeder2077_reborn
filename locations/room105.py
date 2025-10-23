from telebot import types

def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="написать объяснительную"))
    keyboard.add(types.KeyboardButton(text="выпить чай"))
    keyboard.add(types.KeyboardButton(text="Переход: холл"))
    bot.send_message(user['id'], 'Вы в 105', reply_markup=keyboard)

def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете 105')


def user_message(bot, message, user, location, all_users):
    if message == 'выпить чай':
        user['energy'] = min(100, user['energy'] + 10)
        user['water'] = min(100, user['water'] + 20)
        bot.send_message(user['id'], f'Вы выпили чай. Теперь у вас {user["water"]}% воды и {user["energy"]}% энергии')
    elif message == 'написать объяснительную':
        if user['energy'] > 35:
            bot.send_message(user['id'], f'Вы очень долго писали объяснительную')
            user['experience'] = max(0, user['experience'] - 1)
            user["energy"] -= 35
            bot.send_message(user['id'], f'Вы устали, теперь у вас {user["energy"]}% энергии')
        else:
            bot.send_message(user['id'], f'Вы так устали, что не можете даже написать объяснительную')
            bot.send_message(user['id'], f'У вас {user["energy"]}% энергии')
        text=message.text
        if(text!=''):
            bot.send_message(user['id'], f'Вы написали объяснительную')
            user['experience'] = max(0, user['experience'] - 1)
            user["energy"] -=15
        else:
            bot.send_message(user['id'],f'Я вас не понял')
    else:
        bot.send_message(user['id'], 'Я вас не понял')