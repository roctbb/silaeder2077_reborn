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

main_keyboard = create_keyboard([
        'Вылезти из-под ковра', 'Откусить кусочек', 'Занюхнуть ковер (о даа)'
    ])

def user_enters_location(bot, user, location, all_users):
    if user['id'] not in location['data'].keys():
        location['data'][user['id']] = {
            'overSmoked?': False, 
            'smokedTimes': 0,
        }
    bot.send_photo(
        user['id'], 
        'https://storage.geekclass.ru/images/f7c4cd3d-1a0f-4e67-99c9-4eab4a2fc3fd.png', 
        'Вы шли и споткнулись, каким-то образом оказавшись в небольшой комнате под <b>ковром</b>. Воздух пахнет прямо как в других карманных измерениях.', 
        reply_markup=main_keyboard,
        parse_mode='HTML'
    )

def user_leaves_location(bot, user, location, all_users):
    pass
    # bot.send_message(user['id'], 'Вы покидаете подковерное карманное измерение')


def user_message(bot, message, user, location, all_users):
    if message == 'Вылезти из-под ковра':
        from methods import transfer_user, get_location_by_id, get_locations_list
        rndloc = random.choice(get_locations_list())
        while rndloc == 'UnderTheCarpet':
            rndloc = random.choice(get_locations_list())
        rndloc = get_location_by_id(rndloc)

        bot.send_message(
            user['id'], 
            f'Вы вылезаете из-под <b>ковра</b> и оказываетесь в {rndloc['name']}, покидая это прекрасное место.\nВы думаете что было бы неплохо вернуться сюда.',
            parse_mode='HTML'
        )
        transfer_user(user, rndloc['id'])
    elif message == 'Откусить кусочек':
        bot.send_photo(
            user['id'],
            'https://storage.geekclass.ru/images/5ab3038e-4c68-4881-bbfc-5692ab7acdc6.png',  
            f'Вы откусываете небольшой кусочек <b>ковра</b> и жуёте его. Вкус не самый приятный, но насытиться можно.\n<i>+15 Сытость ({user['food']})</i>\n<i>-10 Вода ({user['water']})</i>',
            parse_mode='HTML'
        )
        user['food'] = min(user['food'] + 15, 100)
        user['water'] = max(user['water'] - 10, 0)
    elif message == 'Занюхнуть ковер (о даа)':
        if not location['data'][user['id']]['overSmoked?']:
            rnd = random.randint(3, 15)
            user['energy'] = min(user['energy'] + rnd, 100)
            bot.send_message(
                user['id'], 
                f'Вы глубоко вдыхаете аромат <b>ковра</b>. Ваш разум наполняется странным блаженством, и вы чувствуете прилив энергии.\n<i>+{rnd} Энергия ({user['energy']})</i>',
                parse_mode='HTML'
            )
            location['data'][user['id']]['smokedTimes'] += 1
            if location['data'][user['id']]['smokedTimes'] > 3:
                location['data'][user['id']]['overSmoked?'] = True
        else:
            rnd = random.randint(35, 57)
            user['energy'] = max(0, user['energy'] - rnd)
            bot.send_message(
                user['id'], 
                f'Вы глубоко вдыхаете аромат <b>ковра</b>. И ЛЮТЕЙШЕ ЗАКАШЛИВАЕТЕСЬ, в глазах темнеет и вы вырубаетесь на какое-то время.\nПосле того как просыпаетесь, вы сразу же чувствуете очень сильную слабость, похоже <b>ковер</b> забрал вашу силу.\n<i>-{rnd} Энергия ({user['energy']})</i>',
                parse_mode='HTML'
            )
    else:
        bot.send_message(
            user['id'], 
            '<b>КОВЕР</b> никак не реагирует на ваши действия.',
            parse_mode='HTML'
        )