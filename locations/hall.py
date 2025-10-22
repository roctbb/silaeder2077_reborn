from telebot import types
import random
def user_enters_location(bot, user, location, all_users):
    if 'card' in user['inventory']:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Пойти в потеряшки, может найду что нибудь интересное."))
        keyboard.add(types.KeyboardButton(text="Накричать на охранника."))
        keyboard.add(types.KeyboardButton(text="Просто пойти дальше."))
        bot.send_message(user['id'], 'Вы входите в холл, что вы будете делать?', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Попробовать убежать."))
        keyboard.add(types.KeyboardButton(text="Пойти в 105 взять карточку."))
        bot.send_message(user['id'], 'У вас нет карточки по этому вы подходите к охранникам и записываетесь, что вы будете делать?', reply_markup=keyboard)

def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из холла')
def user_message(bot, message, user, location, all_users):
    global users
    if message == 'Пойти в потеряшки, может найду что нибудь интересное.':
        user['energy'] = max(0, user['energy'] - 5)
        bot.send_message(user['id'], f'Вы покопались в потеряшках, Теперь у вас {user["energy"]} энергии.')
        #добавить сюда лут (сделать функцию в мэйне)
    elif message == 'Попробовать убежать.':
        if random.randint(1,10)>5:
            bot.send_message(user['id'], 'Вас хватают и уводят в 105')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Перейти в 105"))
            bot.send_message(user['id'],'Вам прийдется идти в 105',reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text='Перейти в каб. 116'))
            keyboard.add(types.KeyboardButton(text="Перейти в 105"))
            keyboard.add(types.KeyboardButton(text="Перейти в спортзал"))
            keyboard.add(types.KeyboardButton(text="Перейти в столовая"))
            keyboard.add(types.KeyboardButton(text="Перейти в туалет"))
            bot.send_message(user['id'],'Убегая вы понимаете что нужно спрятаться в одном из кабинетов!',reply_markup=keyboard)
    elif message == "Накричать на охранника.":
        bot.send_message(user['id'], 'Охранник приходит в бешенство, бежит к тебе и отводит в 105.')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Перейти в 105"))
        bot.send_message(user['id'], 'Вам прийдется идти в 105', reply_markup=keyboard)
    elif message == "Пойти в 105 взять карточку.":
        bot.send_message(user['id'], 'Слава богу в этот раз ты идешь в 105 просто за карточкой, а не за объяснительной.')
        user['inventory'].append('card')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Перейти в 105"))
        bot.send_message(user['id'], 'Вам прийдется идти в 105', reply_markup=keyboard)
    elif message == "Просто пойти дальше.":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Перейти в каб. 116'))
        keyboard.add(types.KeyboardButton(text="Перейти в 105"))
        keyboard.add(types.KeyboardButton(text="Перейти в спортзал"))
        keyboard.add(types.KeyboardButton(text="Перейти в столовая"))
        keyboard.add(types.KeyboardButton(text="Перейти в туалет"))
        bot.send_message(user['id'], 'Куда вы пойдете.', reply_markup=keyboard)
    else:
        bot.send_message(user['id'], 'Я вас не понял')