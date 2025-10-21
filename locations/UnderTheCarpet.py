from telebot import types
import random

#---УТИЛИТЫ---

def create_keyboard(buttons, rowsWidth=3):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=rowsWidth)

    for button in buttons:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard

#---БОТ---

main_keyboard = create_keyboard([
        "Вылезти из-под ковра"
    ])

def user_enters_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы шли и споткнулись, каким-то образом оказавшись в небольшой комнате под ковром. Воздух пахнет прямо как в других карманных измерениях.', reply_markup=main_keyboard)


def user_leaves_location(bot, user, location, all_users):
    pass
    # bot.send_message(user['id'], 'Вы покидаете подковерное карманное измерение')


def user_message(bot, message, user, location, all_users):
    if message == 'Вылезти из-под ковра':
        from library import getLocList
        from methods import transfer_user, get_location_by_id
        rndloc = random.choice(getLocList())
        while rndloc == 'UnderTheCarpet':
            rndloc = random.choice(getLocList())
        rndloc = get_location_by_id(rndloc)
        
        bot.send_message(user['id'], f'Вы вылезаете из-под ковра и оказываетесь в {rndloc['name']}, покидая это прекрасное место.\nВы думаете что было бы неплохо вернуться сюда.')
        transfer_user(user, rndloc['id'])
    else:
        bot.send_message(user['id'], 'Комната никак не реагирует на ваши действия.')
