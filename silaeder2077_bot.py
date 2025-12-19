import telebot
from library import users, locations, bot, modules
from methods import *
from telebot import types
from config import TOKEN
import traceback
import datetime


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = get_user(message)
    if not user:
        user = register_user(message)
        send_welcome(user)
        transfer_user(user, 'yard')
    else:
        # Показываем меню независимо от локации
        show_start_menu_from_anywhere(bot, user)


# В функции show_start_menu_from_anywhere добавим новые кнопки:
def show_start_menu_from_anywhere(bot, user):
    """Показывает стартовое меню из любой локации"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="👤 Мой профиль"))
    keyboard.add(types.KeyboardButton(text="📊 Статистика игроков"))
    keyboard.add(types.KeyboardButton(text="📝 Мои объяснительные"))
    keyboard.add(types.KeyboardButton(text="👥 Игроки в комнате"))
    keyboard.add(types.KeyboardButton(text="💬 Написать игроку"))
    keyboard.add(types.KeyboardButton(text="🎮 Продолжить игру"))
    keyboard.add(types.KeyboardButton(text="❓ Помощь"))

    # Собираем информацию о пользователе
    profile_info = f"""
👤 Ваш профиль:
Имя: {user['name']}
Опыт: {user.get('experience', 0)}
Энергия: {user.get('energy', 0)}%
Еда: {user.get('food', 0)}%
Вода: {user.get('water', 0)}%
❤️ HP: {user.get('HP', 100)}/100
💰 Силаэдры: {user.get('silаedry', 0)}

📍 Текущая локация: {get_location_by_id(user.get('location', '')).get('name', 'Неизвестно') if user.get('location') else 'Неизвестно'}

🎒 Инвентарь: {', '.join(user.get('inventory', [])) or 'Пусто'}

📝 Объяснительных: {user.get('obiyasnitelinee', 0)}
"""

    if 'ingas_favorite' in user.get('inventory', []):
        profile_info += "\n❤️ Вы - любимчик Инги Александровны!"

    bot.send_message(user['id'],
                     '🎮 Меню игры:\n\n' + profile_info,
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def process_text(message):
    user = get_user(message)
    print(message.text, users)

    if not user:
        user = register_user(message)
        send_welcome(user)
        transfer_user(user, 'yard')
    else:
        message_text = message.text

        # Обработка команды start в любом месте
        if message_text.lower() == 'start':
            show_start_menu_from_anywhere(bot, user)
            return

        if message_text == "👤 Мой профиль":
            bot.send_message(user['id'], f"Имя: {user['name']}")
            return

        if message_text == "📝 Мои объяснительные":
            bot.send_message(user["id"], "\n".join([i["text"] for i in user['obiyasnitelnay']]))
            return

        if message_text == "👥 Игроки в комнате":
            bot.send_message(user["id"],
                             "Игроки в комнате:\n" + ", ".join([
                                 i["name"] for i in users
                                 if i["location"] == user["location"] and i["id"] != user["id"]]))
            return

        if message_text == "💬 Написать игроку":
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
            return

        if user.get('awaiting_private_message'):
            if message == '↩️ Назад':
                del user['awaiting_private_message']
                show_start_menu_from_anywhere(bot, user)
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
            return

        if user.get('awaiting_message_text'):
            if message == '↩️ Отмена':
                keys_to_remove = ['awaiting_private_message', 'awaiting_message_text',
                                  'private_message_target', 'private_message_target_name']
                for key in keys_to_remove:
                    if key in user:
                        del user[key]
                show_start_menu_from_anywhere(bot, user)
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

                keys_to_remove = ['awaiting_private_message', 'awaiting_message_text',
                                  'private_message_target', 'private_message_target_name']
                for key in keys_to_remove:
                    if key in user:
                        del user[key]
                show_start_menu_from_anywhere(bot, user)
            return

        if message.text == "🎮 Продолжить игру":
            transfer_user(user, user["location"])
            return

        # Обработка переходов
        if message_text.startswith('Переход: '):
            location = get_location_by_name(message_text.replace('Переход: ', ''))
            if location:
                transfer_user(user, location['id'])
            else:
                bot.send_message(user['id'], 'Локация не найдена.')
        else:
            location = get_location_by_id(user['location'])
            neighbours = get_location_users(user['location'])
            try:
                modules[user['location']].user_message(bot, message_text, user, location, neighbours)
            except Exception as e:
                print(e)

    print(users)
    save_state_to_file(users, locations)


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


if __name__ == '__main__':
    load_modules()
    load_state()
    print("Started polling")
    ex = None
    while True:
        try:
            bot.polling(none_stop=True)
        except KeyboardInterrupt:
            break
        except Exception as e:
            if e != ex:
                ex = e
                traceback.print_exc()
