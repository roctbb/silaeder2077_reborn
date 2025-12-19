from telebot import types
import random
from datetime import datetime
from methods import *
from locations.hall_1 import is_lesson_time, drink_water

# Игровое состояние для шашек
CHECKERS_GAMES = {}


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Основные переходы из холла 4 этажа
    keyboard.add(types.KeyboardButton(text="Переход: каб. Физики"))
    keyboard.add(types.KeyboardButton(text="Переход: лестница со 2 на 4 этаж"))

    # Проверяем, можно ли играть в шашки
    other_players = [u for u in all_users if u['id'] != user['id']]
    if other_players:
        keyboard.add(types.KeyboardButton(text="🔴 Играть в шашки"))

    # Кнопка попить воды
    keyboard.add(types.KeyboardButton(text="💧 Попить воды из кулера"))

    bot.send_message(user['id'],
                     'Вы в холле 4 этажа.',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из холла 4 этажа')


def start_checkers_game(bot, user, all_users):
    """Начинает игру в шашки"""
    other_players = [u for u in all_users if u['id'] != user['id']]
    if not other_players:
        bot.send_message(user['id'], 'В холле нет других игроков для игры в шашки')
        return

    # Простая реализация - начинаем игру с первым попавшимся игроком
    opponent = other_players[0]

    # Создаем игру
    game_id = f"checkers_{user['id']}_{opponent['id']}_{datetime.now().timestamp()}"
    CHECKERS_GAMES[game_id] = {
        'player1': user['id'],
        'player2': opponent['id'],
        'turn': 'player1'
    }

    user['current_checkers_game'] = game_id
    opponent['current_checkers_game'] = game_id

    # Простая игра в шашки - случайный результат
    bot.send_message(user['id'], 'Игра в шашки началась! Сделайте ход (например: "с3 d4")')
    bot.send_message(opponent['id'], 'Игра в шашки началась! Ожидайте своего хода.')


def process_checkers_move(bot, user, move):
    """Обрабатывает ход в шашках"""
    game_id = user.get('current_checkers_game')
    if not game_id or game_id not in CHECKERS_GAMES:
        bot.send_message(user['id'], 'У вас нет активной игры в шашки')
        return

    game = CHECKERS_GAMES[game_id]
    opponent_id = game['player2'] if game['player1'] == user['id'] else game['player1']

    # Простая валидация
    if not validate_checkers_move(move):
        bot.send_message(user['id'], 'Неверный формат хода. Используйте: с3 d4')
        return

    # Случайный результат
    result = random.choice(['Ход принят', 'Побил шашку!', 'Стал дамкой!', 'Победа!'])

    bot.send_message(user['id'], f'Ваш ход: {move} - {result}')
    bot.send_message(opponent_id, f'Противник сделал ход: {move}')

    if 'Победа!' in result:
        # Награда за победу
        user['experience'] = user.get('experience', 0) + 8
        user['silаedry'] = user.get('silаedry', 0) + 3

        bot.send_message(user['id'], '🎉 Вы выиграли в шашки!')
        bot.send_message(opponent_id, '😞 Вы проиграли в шашки.')

        del CHECKERS_GAMES[game_id]
        if 'current_checkers_game' in user:
            del user['current_checkers_game']

        user_enters_location(bot, user, None, [])
    else:
        # Меняем ход
        game['turn'] = 'player2' if game['turn'] == 'player1' else 'player1'


def validate_checkers_move(move):
    """Простая валидация хода в шашки"""
    parts = move.split()
    if len(parts) != 2:
        return False

    from_pos, to_pos = parts

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

    elif message == '🔴 Играть в шашки':
        start_checkers_game(bot, user, all_users)
        return

    elif message.startswith('Переход: '):
        location_name = message.replace('Переход: ', '')
        location_map = {
            'каб. Физики': 'room_physics',
            'лестница со 2 на 4 этаж': 'stairs_2_4'
        }

        if location_name in location_map:
            transfer_user(user, location_map[location_name])
        else:
            bot.send_message(user['id'], 'Неизвестный переход')

    else:
        # Проверяем, не является ли это ходом в шашки
        if ' ' in message and len(message.split()) == 2:
            if user.get('current_checkers_game'):
                process_checkers_move(bot, user, message)
                return

        bot.send_message(user['id'], 'Я вас не понял')