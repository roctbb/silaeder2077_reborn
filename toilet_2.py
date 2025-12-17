from telebot import types
import random
from datetime import datetime, timedelta
from methods import *
from locations.toilet_1 import TOILET_PAPER_STOCK, get_toilet_paper_amount


def user_enters_location(bot, user, location, all_users):
    paper_amount = get_toilet_paper_amount('toilet_2')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Взять туалетную бумагу"))

    other_players = [u for u in all_users if u['id'] != user['id']]
    if other_players:
        keyboard.add(types.KeyboardButton(text="Кинуться бумагой в игрока"))

    keyboard.add(types.KeyboardButton(text="Переход: холл 2 этажа"))

    bot.send_message(user['id'],
                     f'Вы в туалете 2 этажа. Туалетной бумаги: {paper_amount} рулонов.',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы вышли из туалета')


def user_message(bot, message, user, location, all_users):
    if message == 'Взять туалетную бумагу':
        paper_amount = get_toilet_paper_amount('toilet_2')

        if paper_amount > 0:
            if random.randint(1, 10) == 1:
                bot.send_message(user['id'], 'В туалет зашла Инга Александровна! "Что ты тут делаешь?! Быстро в 105!"')
                user['ochota'] = 2
                transfer_user(user, 'room105')
                return

            TOILET_PAPER_STOCK['toilet_2']["amount"] -= 1
            if 'toilet_paper' not in user['inventory']:
                user['inventory'].append('toilet_paper')

            bot.send_message(user['id'],
                             f'Вы взяли рулон туалетной бумаги. Осталось: {TOILET_PAPER_STOCK["toilet_2"]["amount"]} рулонов.')

            paper_count = len([item for item in user['inventory'] if item == 'toilet_paper'])
            if paper_count > 5:
                bot.send_message(user['id'], 'У вас слишком много туалетной бумаги!')
        else:
            bot.send_message(user['id'], 'Туалетная бумага закончилась!')

    elif message == 'Кинуться бумагой в игрока':
        if 'toilet_paper' not in user['inventory']:
            bot.send_message(user['id'], 'У вас нет туалетной бумаги!')
            return

        other_players = [u for u in all_users if u['id'] != user['id']]
        if not other_players:
            bot.send_message(user['id'], 'В туалете больше никого нет!')
            return

        target = random.choice(other_players)
        user['inventory'].remove('toilet_paper')
        target['cannot_play_until'] = (datetime.now() + timedelta(minutes=1)).isoformat()

        bot.send_message(user['id'],
                         f'Вы кинулись туалетной бумагой в {target["name"]}! Теперь он не может играть 1 минуту.')

        bot.send_message(target['id'],
                         f'{user["name"]} кинулся в вас туалетной бумагой! Вы не можете играть 1 минуту.')

    elif message.startswith('Переход: '):
        location_name = message.replace('Переход: ', '')
        if location_name == 'холл 2 этажа':
            transfer_user(user, 'hall_2')
        else:
            bot.send_message(user['id'], 'Отсюда можно выйти только в холл 2 этажа')

    else:
        bot.send_message(user['id'], 'Я вас не понял')