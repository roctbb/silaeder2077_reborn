from telebot import types


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отдохнуть на лавочке"))
    bot.send_message(user['id'], 'Вы во дворе', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы спорт зал Дениса')


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть на лавочке':
        user['energy'] = min(100, user['energy'] + 5)
        bot.send_message(user['id'], f'Вы передохнули на лавочке, пару минут. Теперь у вас {user["energy"]} энергии.')
    else:
        bot.send_message(user['id'], 'Я вас не понял')

