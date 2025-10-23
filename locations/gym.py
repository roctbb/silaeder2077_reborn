from telebot import types
import random

def make_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поиграть в волейбол"))
    keyboard.add(types.KeyboardButton(text="Поискать что-нибудь интересное"))
    keyboard.add(types.KeyboardButton(text="Попинать мячик пока учитель не видет"))
    keyboard.add(types.KeyboardButton(text="Попить водички"))
    keyboard.add(types.KeyboardButton(text="Переход: двор"))

    return keyboard

def user_enters_location(bot, user, location, all_users):

    bot.send_message(user['id'], 'Вы в спортзале', reply_markup=make_default_keyboard())


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули спортзал Дениса')


def user_message(bot, message, user, location, all_users):
    if message == 'Поиграть в волейбол':
        if user['energy']>=5 and  user['water']>=5:
            user['energy'] = user['energy'] - 5
            user['water'] = user['water'] - 5
            x=random.randint(1,3)
            if x == 1:
                user['experience'] = user['experience'] + 1
                bot.send_message(user['id'], f'Вам повезло и вы смогли заработать опыта теперь у вас {user["experience"]} опыта')
            else:
                bot.send_message(user['id'], f'Вам не повезло и вы не смогли заработать опыта сейчас у вас {user["experience"]} опыта')
            bot.send_message(user['id'], f'Вы потратили энергию и воду теперь у вас {user["energy"]}% энергии, и {user["water"]}% воды.')
        else:
            if user['energy']<5 and  user['water']<5:
                bot.send_message(user['id'], f'У вас не хватает энергии и воды! Сейчас у вас {user["energy"]}% энергии, и {user["water"]}% воды. А нужно всего 5% энергии и воды!')
            elif user['energy']<5:
                bot.send_message(user['id'], f'У вас не хватает энергии! Сейчас у вас {user["energy"]}% энергии.  нужно всего 5% энергии и воды!')
            else:
                bot.send_message(user['id'], f'У вас не хватает воды! Сейчас у вас {user["water"]}% воды. А нужно всего 5% воды!')
    elif message == 'Попить водички':
        user['water'] = min(100,user['water'] + 5)
        bot.send_message(user['id'], f'Вы попили воду теперь у вас {user["water"]}% воды.')
    elif message == 'Попинать мячик пока учитель не видет':
        x=random.randint(1,2)
        if x==1:
            bot.send_message(user['id'], f'Вы начали пинать мячик и вас спалил учитель!')
            x2=random.randint(1,2)
            if x2==1:
                bot.send_message(user['id'], f'Похоже тебе не повезло в двойне и у учителя нет настроения! Так бы он отправил писать объяснительную, но тебе повело и я ещё не написал эту функцию, но вскоре такое не прокатит!!!')
            else:
                bot.send_message(user['id'], f'Похоже тебе повезло и у учителя хорошее настроение! На этот раз он тебя простил!')
        else:
            user['experience'] = user['experience'] + 1
            bot.send_message(user['id'], f'Похоже тебе повезло и учитель тебя не заметил! Лави опыт! Теперь у тебя {user["experience"]} опыта!')
    elif message == 'Поискать что-нибудь интересное':
        x = random.randint(1, 2)
        if x == 1:
            bot.send_message(user['id'], 'Вам очень повезло и вы нашли компьютер')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Поиграть в майнкрафт"))
            keyboard.add(types.KeyboardButton(text="Переход: двор"))
            bot.send_message(user['id'], 'Там был запущен майнкрафт что будешь с этим делать?', reply_markup=keyboard)
        else:
                bot.send_message(user['id'], 'Вам не повезло и вы не нашли ничего')
    elif message == 'Поиграть в майнкрафт':
        x = random.randint(1, 2)
        if x == 1:
            bot.send_message(user['id'], 'Вам не повезло и вы идёте писать объяснительную! Потому-что вас застукали учителя!')
        else:
            user['experience'] = user['experience'] + 1
            bot.send_message(user['id'], f'Лови опыт теперь у тебя {user["experience"]} опыта!')
        bot.send_message(user['id'], 'Вы в спортзале', reply_markup=make_default_keyboard())
    else:
        bot.send_message(user['id'], 'Я вас не понял')

