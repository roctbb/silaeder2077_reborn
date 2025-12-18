import telebot
from library import users, locations, bot, modules
from methods import *
from telebot import types
from config import TOKEN
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


if __name__ == '__main__':
    load_modules()
    load_state()
    bot.polling(none_stop=True)