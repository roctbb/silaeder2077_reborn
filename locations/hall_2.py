from telebot import types
import random
from datetime import datetime
from methods import *
from locations.hall_1 import is_lesson_time, drink_water, LESSON_SCHEDULE

# Игровое состояние для шахмат
CHESS_GAMES = {}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Основные переходы из холла 2 этажа
    keyboard.add(types.KeyboardButton(text="Переход: туалет 2 этажа"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. Математики"))
    keyboard.add(types.KeyboardButton(text="Переход: каб. CTF"))
    keyboard.add(types.KeyboardButton(text="Переход: теннисный стол"))
    keyboard.add(types.KeyboardButton(text="Переход: лестница с 1 на 2 этаж"))
    keyboard.add(types.KeyboardButton(text="Переход: лестница со 2 на 4 этаж"))

    # Проверяем, можно ли играть в шахматы
    other_players = [u for u in all_users if u['id'] != user['id']]
    if other_players:
        keyboard.add(types.KeyboardButton(text="♟️ Играть в мысленные шахматы"))

    # Кнопка попить воды
    keyboard.add(types.KeyboardButton(text="💧 Попить воды из кулера"))

    bot.send_message(user['id'],
                     'Вы в холле 2 этажа.',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из холла 2 этажа')


def start_chess_game(bot, user, all_users):
    """Начинает игру в шахматы"""
    # Находим противника
    other_players = [u for u in all_users if u['id'] != user['id']]
    if not other_players:
        bot.send_message(user['id'], 'В холле нет других игроков для игры в шахматы')
        return

    # Предлагаем выбрать противника
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opponent in other_players:
        keyboard.add(types.KeyboardButton(text=f"♟️ Играть с {opponent['name']}"))
    keyboard.add(types.KeyboardButton(text="↩️ Отмена"))

    user['awaiting_chess_opponent'] = True
    bot.send_message(user['id'], 'Выберите противника:', reply_markup=keyboard)


def process_chess_move(bot, user, move):
    """Обрабатывает ход в шахматах"""
    game_id = user.get('current_chess_game')
    if not game_id or game_id not in CHESS_GAMES:
        bot.send_message(user['id'], 'У вас нет активной шахматной игры')
        return

    game = CHESS_GAMES[game_id]

    # Простая валидация хода (формат: e2 e4)
    if not validate_chess_move(move):
        bot.send_message(user['id'], 'Неверный формат хода. Используйте: e2 e4')
        return

    # Здесь должна быть реальная логика шахмат
    # Для простоты делаем случайный результат

    opponent_id = game['white'] if game['black'] == user['id'] else game['black']

    # Отправляем ход противнику
    bot.send_message(opponent_id, f"{user['name']} сделал ход: {move}")

    # Случайный результат
    result = random.choice(['Ход принят', 'Некорректный ход', 'Шах!', 'Мат!'])

    if 'Мат!' in result:
        # Завершаем игру
        winner = user['id']
        loser = opponent_id

        bot.send_message(winner, '🎉 Вы выиграли!')
        bot.send_message(loser, '😞 Вы проиграли.')

        # Награда за победу
        user['experience'] = user.get('experience', 0) + 10
        user['silаedry'] = user.get('silаedry', 0) + 5

        # Удаляем игру
        del CHESS_GAMES[game_id]
        if 'current_chess_game' in user:
            del user['current_chess_game']

        # Возвращаем в холл
        user_enters_location(bot, user, None, [])
    else:
        bot.send_message(user['id'], f'Результат: {result}')
        # Продолжаем игру...


def validate_chess_move(move):
    """Простая валидация шахматного хода"""
    parts = move.split()
    if len(parts) != 2:
        return False

    from_pos, to_pos = parts

    # Проверяем формат (буква + цифра)
    if len(from_pos) != 2 or len(to_pos) != 2:
        return False

    if not ('a' <= from_pos[0] <= 'h') or not ('1' <= from_pos[1] <= '8'):
        return False

    if not ('a' <= to_pos[0] <= 'h') or not ('1' <= to_pos[1] <= '8'):
        return False

    return True


def user_message(bot, message, user, location, all_users):
    if message == '💧 Попить воды из кулера':
        drink_water(bot, user)
        user_enters_location(bot, user, location, all_users)
        return

    elif message == '♟️ Играть в мысленные шахматы':
        start_chess_game(bot, user, all_users)
        return

    elif user.get('awaiting_chess_opponent'):
        if message == '↩️ Отмена':
            del user['awaiting_chess_opponent']
            user_enters_location(bot, user, location, all_users)
            return

        # Обработка выбора противника
        if message.startswith('♟️ Играть с '):
            opponent_name = message.replace('♟️ Играть с ', '')
            opponent = None

            for u in all_users:
                if u['name'] == opponent_name and u['id'] != user['id']:
                    opponent = u
                    break

            if opponent:
                # Создаем игру
                game_id = f"{user['id']}_{opponent['id']}_{datetime.now().timestamp()}"
                CHESS_GAMES[game_id] = {
                    'white': user['id'],
                    'black': opponent['id'],
                    'board': 'start',  # Здесь должно быть состояние доски
                    'turn': 'white'
                }

                user['current_chess_game'] = game_id
                opponent['current_chess_game'] = game_id

                del user['awaiting_chess_opponent']

                bot.send_message(user['id'],
                                 f'Игра началась! Вы играете белыми.\n'
                                 f'Введите ход в формате: e2 e4')
                bot.send_message(opponent['id'],
                                 f'{user["name"]} пригласил вас в шахматы! Вы играете чёрными.\n'
                                 f'Ожидайте своего хода.')
            else:
                bot.send_message(user['id'], 'Игрок не найден')

    elif message.startswith('Переход: '):
        location_name = message.replace('Переход: ', '')
        location_map = {
            'туалет 2 этажа': 'toilet_2',
            'каб. Математики': 'math',
            'лестница с 1 на 2 этаж': 'stairs_1_2',
            'лестница со 2 на 4 этаж': 'stairs_2_4'
        }

        if location_name in location_map:
            transfer_user(user, location_map[location_name])
        else:
            bot.send_message(user['id'], 'Неизвестный переход')

    else:
        # Проверяем, не является ли это ходом в шахматы
        if ' ' in message and len(message.split()) == 2:
            if user.get('current_chess_game'):
                process_chess_move(bot, user, message)
                return

        bot.send_message(user['id'], 'Я вас не понял')