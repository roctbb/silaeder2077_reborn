from telebot import types


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Перейти: двор"))
    bot.send_message(user['id'], 'Вы дома!', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите их дома')


def user_message(bot, message, user, location, all_users):
    bot.send_message(user['id'], 'Я вас не понял')