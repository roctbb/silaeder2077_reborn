from telebot import types


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть на лавочке"))
    keyboard.add(types.KeyboardButton(text="Переход: спортзал"))
    keyboard.add(types.KeyboardButton(text="Переход: задний двор"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. 116"))
    keyboard.add(types.KeyboardButton(text="Переход: холл"))
    keyboard.add(types.KeyboardButton(text="Переход: туалет"))
    keyboard.add(types.KeyboardButton(text="Переход: математика"))
    bot.send_message(user['id'], 'Вы во дворе', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете двор')

def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть на лавочке':
        user['energy'] = min(100, user['energy'] + 5)
        bot.send_message(user['id'], f'Вы передохнули на лавочке, пару минут. Теперь у вас {user["energy"]}% энергии.')
    else:
        bot.send_message(user['id'], 'Я вас не понял')
