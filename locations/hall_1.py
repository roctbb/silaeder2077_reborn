from telebot import types
import random
from datetime import datetime, timedelta
from methods import *

# Расписание уроков
LESSON_SCHEDULE = [
    (9, 0, 9, 40),  # 1 урок
    (9, 45, 10, 25),  # 2 урок
    (10, 45, 11, 25),  # 3 урок
    (11, 45, 12, 25),  # 4 урок
    (12, 30, 13, 10),  # 5 урок
    (13, 50, 14, 30),  # 6 урок
    (14, 35, 15, 15),  # 7 урок
    (15, 20, 16, 0)  # 8 урок
]


def is_lesson_time():
    """Проверяет, идет ли сейчас урок"""
    now = datetime.now()

    for lesson_start_h, lesson_start_m, lesson_end_h, lesson_end_m in LESSON_SCHEDULE:
        lesson_start = now.replace(hour=lesson_start_h, minute=lesson_start_m, second=0)
        lesson_end = now.replace(hour=lesson_end_h, minute=lesson_end_m, second=0)

        if lesson_start <= now <= lesson_end:
            return True

    return False


def make_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Основные переходы из холла 1 этажа
    keyboard.add(types.KeyboardButton(text="Переход: лестница с 1 на 2 этаж"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. 105"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. 116"))
    keyboard.add(types.KeyboardButton(text="Переход: комната охраны"))
    keyboard.add(types.KeyboardButton(text="Переход: двор"))
    keyboard.add(types.KeyboardButton(text="Переход: задний двор"))
    keyboard.add(types.KeyboardButton(text="Переход: столовая"))
    keyboard.add(types.KeyboardButton(text="Переход: спортзал"))

    # Кнопка попить воды
    keyboard.add(types.KeyboardButton(text="💧 Попить воды из кулера"))

    return keyboard


def handle_105_transition(bot, user):
    """Обработка перехода в кабинет 105"""
    # Если нет карточки - отправляем с целью взять карточку
    if 'card' not in user['inventory']:
        user['ochota'] = 0  # Цель: взять карточку
        bot.send_message(user['id'],
                         'Вы направляетесь в кабинет 105, чтобы получить карточку у Инги Александровны.')
    else:
        # Если есть карточка, но переходим в 105 - случайная цель
        choice = random.randint(1, 3)
        if choice == 1:
            user['ochota'] = 1  # Просто пришел
            bot.send_message(user['id'],
                             'Вы заходите в кабинет 105 просто так...')
        else:
            user['ochota'] = 2  # Пришел писать объяснительную
            bot.send_message(user['id'],
                             'Инга Александровна: "А, это ты! Садись, нужно поговорить..."')

    # Переход в 105
    location_obj = get_location_by_name('каб. 105')
    if location_obj:
        transfer_user(user, location_obj['id'])


def user_enters_location(bot, user, location, all_users):
    # Сбрасываем счетчик выходов если начался новый урок
    now = datetime.now()
    reset_time = user.get('hall_exits_reset_time')

    if reset_time:
        reset_dt = datetime.fromisoformat(reset_time)
        # Если прошло больше 45 минут (длительность урока), сбрасываем счетчик
        if now - reset_dt > timedelta(minutes=45):
            user['hall_exits_count'] = 0

    # Проверяем наличие карточки
    if 'card' in user['inventory']:
        # Если есть карточка, стандартное меню
        bot.send_message(user['id'], 'Вы входите в холл 1 этажа. У вас есть карточка, охрана вас пропускает.')
        bot.send_message(user['id'], 'Куда хотите пойти?', reply_markup=make_default_keyboard())
    else:
        # Нет карточки - общение с охраной
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Попробовать убежать"))
        keyboard.add(types.KeyboardButton(text="Пойти в 105 взять карточку"))
        keyboard.add(types.KeyboardButton(text="Объясниться с охраной"))

        bot.send_message(user['id'],
                         'У вас нет карточки. Охранник останавливает вас: "Эй, студент! Где твоя карточка?"',
                         reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из холла 1 этажа')


def drink_water(bot, user):
    """Попить воды из кулера"""
    user['water'] = min(100, user.get('water', 0) + 15)
    user['energy'] = min(100, user.get('energy', 0) + 5)

    bot.send_message(user['id'],
                     f'Вы попили воды из кулера. +15% воды, +5% энергии.\n'
                     f'Теперь у вас {user["water"]}% воды и {user["energy"]}% энергии.')


def user_message(bot, message, user, location, all_users):
    # Всегда обрабатываем команду start
    if message.lower() == 'start' or message == '/start':
        show_start_menu_from_anywhere(bot, user)
        return

    # Обработка питья воды
    if message == '💧 Попить воды из кулера':
        drink_water(bot, user)
        user_enters_location(bot, user, location, all_users)
        return

    # Проверяем наличие карточки для обработки основного меню
    if 'card' in user['inventory']:
        # Если есть карточка, обрабатываем переходы
        if message.startswith('Переход: '):
            location_name = message.replace('Переход: ', '')

            if location_name == 'каб. 105':
                # Специальная обработка перехода в 105
                handle_105_transition(bot, user)
            else:
                # Стандартный переход
                location_map = {
                    'лестница с 1 на 2 этаж': 'stairs_1_2',
                    'каб. 116': 'room116',
                    'комната охраны': 'security',
                    'двор': 'yard',
                    'задний двор': 'back_yard',
                    'столовая': 'dining_room',
                    'спортзал': 'gym'
                }

                if location_name in location_map:
                    transfer_user(user, location_map[location_name])
                else:
                    bot.send_message(user['id'], 'Локация не найдена.')

        # Обработка других сообщений (из старого кода)
        elif message == 'Пойти в потеряшки, может найду что нибудь интересное':
            user['energy'] = max(0, user['energy'] - 5)
            if random.randint(1, 10) < 5:
                user['food'] = min(100, user['food'] + random.randint(1, 15))
                bot.send_message(user['id'],
                                 f'Вы покопались в потеряшках. Теперь у вас {user["energy"]} энергии и {user["food"]} еды')
                bot.send_message(user['id'],
                                 'Вы нашли кусок хлеба и сьели его, но вы услышали шаги разгневанной Инги Александровны и решили сбежать')
            else:
                user['water'] = min(100, user['water'] + random.randint(1, 15))
                bot.send_message(user['id'],
                                 f'Вы покопались в потеряшках. Теперь у вас {user["energy"]} энергии и {user["water"]} воды')
                bot.send_message(user['id'],
                                 'Вы нашли бутылку воды и выпили её, но вы услышали шаги разгневанной Инги Александровны и решили сбежать')
            bot.send_message(user['id'], 'Куда вы убежите!', reply_markup=make_default_keyboard())

        elif message == "Накричать на охранника":
            # Обновленная логика с уточнением
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Пойти в 105"))
            keyboard.add(types.KeyboardButton(text="Попытаться убежать"))
            bot.send_message(user['id'],
                             'Охранник приходит в бешенство: "Быстро в 105 на объяснительную!" Что будешь делать?',
                             reply_markup=keyboard)

        else:
            bot.send_message(user['id'], 'Я вас не понял')

    else:
        # Если нет карточки
        if message == 'Попробовать убежать':
            if random.randint(1, 10) > 5:
                bot.send_message(user['id'], 'Вас хватают и уводят в 105')
                user['ochota'] = 2  # Пришел писать объяснительную
                transfer_user(user, 'room105')
            else:
                bot.send_message(user['id'], 'Убегая вы понимаете что нужно спрятаться в одном из кабинетов!')
                # Добавляем карточку в качестве награды за успешный побег
                user['inventory'].append('card')
                bot.send_message(user['id'], 'Вы успешно сбежали и нашли потерянную карточку!',
                                 reply_markup=make_default_keyboard())

        elif message == "Пойти в 105 взять карточку":
            user['ochota'] = 0  # Цель: взять карточку
            bot.send_message(user['id'],
                             'Вы направляетесь в кабинет 105, чтобы получить карточку у Инги Александровны.')
            transfer_user(user, 'room105')

        elif message == "Объясниться с охраной":
            explanations = [
                "Я новенький, мне еще не выдали карточку",
                "Я потерял карточку, можно получить новую?",
                "Простите, забыл карточку дома",
                "Моя карточка сломалась, нужно заменить"
            ]
            explanation = random.choice(explanations)

            if random.randint(1, 2) == 1:
                # Повезло - отпускают
                user['inventory'].append('card')
                bot.send_message(user['id'],
                                 f'Охранник: "{explanation}? Ладно, в этот раз поверю. Вот временная карточка."\n'
                                 f'Вы получили карточку!',
                                 reply_markup=make_default_keyboard())
            else:
                # Не повезло - отправляют в 105
                bot.send_message(user['id'],
                                 f'Охранник: "{explanation}? Иди к Инге Александровне в 105, пусть разбирается."')
                user['ochota'] = 0  # Цель: взять карточку
                transfer_user(user, 'room105')

        elif message == "Пойти в 105":
            # Если выбрали пойти в 105 после крика на охранника
            user['ochota'] = 2  # Пришел писать объяснительную
            transfer_user(user, 'room105')

        elif message == "Попытаться убежать":
            # Если выбрали убежать после крика на охранника
            if random.randint(1, 4) < 4:  # Шанс 3 к 4
                bot.send_message(user['id'],
                                 'Вы пытаетесь убежать, но охрана вас ловит! "Теперь точно в 105!"')
                user['ochota'] = 2  # Пришел писать объяснительную
                transfer_user(user, 'room105')
            else:
                bot.send_message(user['id'], 'Вам удалось сбежать!')
                # Возвращаем обычное меню
                if 'card' in user['inventory']:
                    bot.send_message(user['id'], 'Куда хотите пойти?', reply_markup=make_default_keyboard())
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.KeyboardButton(text="Попробовать убежать"))
                    keyboard.add(types.KeyboardButton(text="Пойти в 105 взять карточку"))
                    keyboard.add(types.KeyboardButton(text="Объясниться с охраной"))
                    bot.send_message(user['id'], 'Охранник: "Ну что, решил?"', reply_markup=keyboard)

        else:
            bot.send_message(user['id'], 'Я вас не понял')