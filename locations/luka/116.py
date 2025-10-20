from telebot import types


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поиграть на пианино"))
    keyboard.add(types.KeyboardButton(text="Потыкать по доске"))
    bot.send_message(user['id'], 'Вы в каб. 116', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули каб. 116')


def user_message(bot, message, user, location, all_users):
    if message == 'Поиграть на пианино':
        user['energy'] = min(100, user['energy'] + 5)
        bot.send_message(user['id'], f'Вы поиграли на пианино'
                                     f'У вас ничего не изменилось ¯\_(ツ)_/¯')
    elif message == 'Потыкать по доске':
        user['energy'] = min(100, user['energy'] + 5)
        user['experience'] = min(100, user['experience'] + 5)
        bot.send_message(user['id'], f'Вы поиграли на пианино'
                                     f'У вас теперь {user['energy']} энергии и {user['experience']} опыта :)')

    else:
        bot.send_message(user['id'], 'Я вас не понял :(')
