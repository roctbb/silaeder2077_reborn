from telebot import types
import random
from methods import *
from library import users


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="👀 Посмотреть камеры"))
    keyboard.add(types.KeyboardButton(text="🗝️ Взять ключи"))
    keyboard.add(types.KeyboardButton(text="💬 Написать игроку"))
    keyboard.add(types.KeyboardButton(text="👥 Кто в комнате?"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))
    bot.send_message(user['id'], 'Вы пришли к комнате охраны', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули комнату охраны')


def show_cameras(bot, user):
    """Показывает, какие игроки в каких локациях"""
    from library import locations
    from methods import get_location_by_id

    camera_info = "📹 Камеры наблюдения:\n\n"

    # Сортируем локации по этажам
    locations_by_floor = {}
    for loc in locations:
        # Извлекаем номер этажа из названия
        floor = "Неизвестно"
        if "1 этаж" in loc['name'] or loc['id'] in ['hall_1', 'toilet_1']:
            floor = "1 этаж"
        elif "2 этаж" in loc['name'] or loc['id'] in ['hall_2', 'toilet_2', 'math']:
            floor = "2 этаж"
        elif "4 этаж" in loc['id'] or loc['id'] == 'room_physics':
            floor = "4 этаж"
        elif loc['id'] in ['yard', 'back_yard', 'dining_room', 'gym']:
            floor = "1 этаж (улица)"
        elif loc['id'] == 'home':
            floor = "Вне школы"

        if floor not in locations_by_floor:
            locations_by_floor[floor] = []

        # Находим игроков в этой локации
        players_in_location = [u for u in users if u.get('location') == loc['id']]
        if players_in_location:
            locations_by_floor[floor].append((loc, players_in_location))

    # Выводим информацию по этажам
    for floor, locs in sorted(locations_by_floor.items()):
        if locs:  # Только если есть локации с игроками на этом этаже
            camera_info += f"=== {floor} ===\n"
            for loc, players in locs:
                player_names = ", ".join([p['name'] for p in players])
                camera_info += f"📍 {loc['name']}: {player_names if player_names else 'Нет игроков'}\n"
            camera_info += "\n"

    if camera_info == "📹 Камеры наблюдения:\n\n":
        camera_info += "На камерах никого нет."

    return camera_info


def get_players_in_same_location(user_id):
    """Получает список игроков в той же локации"""
    current_user = next((u for u in users if u['id'] == user_id), None)
    if not current_user or not current_user.get('location'):
        return []

    location_id = current_user['location']
    return [u for u in users if u['id'] != user_id and u.get('location') == location_id]


def user_message(bot, message, user, location, all_users):
    if message == '👀 Посмотреть камеры':
        camera_info = show_cameras(bot, user)
        bot.send_message(user['id'], camera_info)

    elif message == '🗝️ Взять ключи':
        if 'keys' not in user['inventory']:
            user['inventory'].append('keys')
            bot.send_message(user['id'], '✅ Вы взяли ключи от кабинетов! Теперь вы можете открывать закрытые двери.')
        else:
            bot.send_message(user['id'], 'У вас уже есть ключи!')

    elif message == '💬 Написать игроку':
        # Показываем список всех игроков
        other_players = [u for u in users if u['id'] != user['id']]
        if not other_players:
            bot.send_message(user['id'], 'Нет других игроков онлайн.')
            return

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for player in other_players:
            player_location = get_location_by_id(player.get('location', ''))
            location_name = player_location.get('name', 'Неизвестно') if player_location else 'Неизвестно'
            keyboard.add(types.KeyboardButton(f"💬 {player['name']} ({location_name})"))

        keyboard.add(types.KeyboardButton("↩️ Назад"))
        user['awaiting_private_message'] = True
        bot.send_message(user['id'], 'Выберите игрока для отправки сообщения:', reply_markup=keyboard)

    elif user.get('awaiting_private_message'):
        if message == '↩️ Назад':
            del user['awaiting_private_message']
            user_enters_location(bot, user, location, all_users)
        elif message.startswith('💬 '):
            # Извлекаем имя игрока
            target_name = message[2:].split(' (')[0]
            target_user = next((u for u in users if u['name'] == target_name and u['id'] != user['id']), None)

            if target_user:
                user['private_message_target'] = target_user['id']
                user['private_message_target_name'] = target_name
                del user['awaiting_private_message']

                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton("↩️ Отмена"))
                bot.send_message(user['id'],
                                 f'Напишите сообщение для {target_name}:\n(максимум 200 символов)',
                                 reply_markup=keyboard)
                user['awaiting_message_text'] = True
            else:
                bot.send_message(user['id'], 'Игрок не найден.')

    elif user.get('awaiting_message_text'):
        if message == '↩️ Отмена':
            cleanup_private_message_state(user)
            user_enters_location(bot, user, location, all_users)
        else:
            if len(message) > 200:
                bot.send_message(user['id'], 'Сообщение слишком длинное! Максимум 200 символов.')
                return

            target_id = user.get('private_message_target')
            target_name = user.get('private_message_target_name')

            if target_id:
                bot.send_message(target_id,
                                 f'📨 Сообщение от {user["name"]} (комната охраны):\n\n{message}')
                bot.send_message(user['id'],
                                 f'✅ Сообщение отправлено игроку {target_name}!')

                # Сохраняем в историю переписки
                save_message_to_history(user['id'], target_id, message, user['name'], 'отправлено')
                save_message_to_history(target_id, user['id'], message, user['name'], 'получено')

            cleanup_private_message_state(user)
            user_enters_location(bot, user, location, all_users)

    elif message == '👥 Кто в комнате?':
        players_here = get_players_in_same_location(user['id'])
        if players_here:
            players_list = "\n".join([f"👤 {p['name']}" for p in players_here])
            bot.send_message(user['id'], f'С вами в комнате охраны:\n\n{players_list}')
        else:
            bot.send_message(user['id'], 'Вы в комнате охраны одни.')

    elif message == 'Переход: холл 1 этажа':
        transfer_user(user, 'hall_1')

    else:
        bot.send_message(user['id'], 'Я вас не понял :(')


def cleanup_private_message_state(user):
    """Очищает состояние отправки приватных сообщений"""
    keys_to_remove = ['awaiting_private_message', 'awaiting_message_text',
                      'private_message_target', 'private_message_target_name']
    for key in keys_to_remove:
        if key in user:
            del user[key]


def save_message_to_history(sender_id, receiver_id, message, sender_name, status):
    """Сохраняет сообщение в историю"""
    for u in users:
        if u['id'] == sender_id or u['id'] == receiver_id:
            if 'message_history' not in u:
                u['message_history'] = []

            u['message_history'].append({
                'from': sender_name,
                'to': receiver_id,
                'message': message,
                'status': status,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Ограничиваем историю 50 сообщениями
            if len(u['message_history']) > 50:
                u['message_history'] = u['message_history'][-50:]