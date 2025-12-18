from telebot import types
from methods import *
from datetime import datetime


def user_enters_location(bot, user, location, all_users):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Пойти в школу!"))
    keyboard.add(types.KeyboardButton(text="🛒 Магазин Силаэдров"))
    keyboard.add(types.KeyboardButton(text="💤 Отдохнуть (восстановить 50 энергии)"))

    # Показываем баланс Силаэдров
    silaedry = user.get('silаedry', 0)
    bot.send_message(user['id'],
                     f'Вы дома! У вас {silaedry} Силаэдров.\n'
                     f'Присоединяйтесь к нашему тг каналу: https://t.me/+tJMzrFckTCUxOTFi',
                     reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы уходите из дома')


def show_shop(bot, user):
    """Показывает магазин товаров за Силаэдры"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Товары в магазине
    items = [
        {"name": "📡 Фейк-сигнализация", "price": 50, "desc": "Выводит Ингу Александровну на 10 минут",
         "id": "fake_alarm"},
        {"name": "📝 Отмена объяснительной", "price": 100, "desc": "Отменяет написание объяснительной",
         "id": "cancel_explanation"},
        {"name": "🍔 Набор еды", "price": 20, "desc": "Восстанавливает 50 еды", "id": "food_pack"},
        {"name": "💧 Набор воды", "price": 20, "desc": "Восстанавливает 50 воды", "id": "water_pack"},
        {"name": "⚡ Энергетик", "price": 30, "desc": "Восстанавливает 50 энергии", "id": "energy_drink"},
        {"name": "❤️ Аптечка", "price": 40, "desc": "Восстанавливает 50 HP", "id": "medkit"},
        {"name": "🎫 Карточка студента", "price": 150, "desc": "Постоянная карточка (если потерял)",
         "id": "student_card"},
        {"name": "🔙 Назад", "price": 0, "desc": "Вернуться домой", "id": "back"}
    ]

    for item in items:
        if item['id'] != 'back':
            keyboard.add(types.KeyboardButton(f"{item['name']} - {item['price']} Силаэдров"))
        else:
            keyboard.add(types.KeyboardButton(item['name']))

    silaedry = user.get('silаedry', 0)
    shop_text = f"🛒 Магазин Силаэдров\nВаш баланс: {silaedry} Силаэдров\n\n"

    for item in items:
        if item['id'] != 'back':
            shop_text += f"{item['name']}\n"
            shop_text += f"   {item['desc']}\n"
            shop_text += f"   Цена: {item['price']} Силаэдров\n\n"

    bot.send_message(user['id'], shop_text, reply_markup=keyboard)


def process_purchase(bot, user, item_name):
    """Обрабатывает покупку товара"""
    items = {
        "📡 Фейк-сигнализация - 50 Силаэдров": {"price": 50, "id": "fake_alarm"},
        "📝 Отмена объяснительной - 100 Силаэдров": {"price": 100, "id": "cancel_explanation"},
        "🍔 Набор еды - 20 Силаэдров": {"price": 20, "id": "food_pack"},
        "💧 Набор воды - 20 Силаэдров": {"price": 20, "id": "water_pack"},
        "⚡ Энергетик - 30 Силаэдров": {"price": 30, "id": "energy_drink"},
        "❤️ Аптечка - 40 Силаэдров": {"price": 40, "id": "medkit"},
        "🎫 Карточка студента - 150 Силаэдров": {"price": 150, "id": "student_card"}
    }

    if item_name not in items:
        return False

    item = items[item_name]
    price = item['price']
    silaedry = user.get('silаedry', 0)

    if silaedry < price:
        bot.send_message(user['id'], f"Недостаточно Силаэдров! Нужно {price}, у вас {silaedry}.")
        return False

    # Списание Силаэдров
    user['silаedry'] = silaedry - price

    # Выдача товара
    if item['id'] == 'fake_alarm':
        if 'fake_alarm' not in user['inventory']:
            user['inventory'].append('fake_alarm')
        bot.send_message(user['id'],
                         "✅ Вы купили фейк-сигнализацию! Используйте в кабинете 105, чтобы вывести Ингу Александровну на 10 минут.")

    elif item['id'] == 'cancel_explanation':
        if 'explanation_cancel' not in user['inventory']:
            user['inventory'].append('explanation_cancel')
        bot.send_message(user['id'],
                         "✅ Вы купили отмену объяснительной! Используйте при написании объяснительной.")

    elif item['id'] == 'food_pack':
        user['food'] = min(100, user.get('food', 0) + 50)
        bot.send_message(user['id'], f"✅ Вы восстановили 50 еды! Теперь у вас {user['food']}% еды.")

    elif item['id'] == 'water_pack':
        user['water'] = min(100, user.get('water', 0) + 50)
        bot.send_message(user['id'], f"✅ Вы восстановили 50 воды! Теперь у вас {user['water']}% воды.")

    elif item['id'] == 'energy_drink':
        user['energy'] = min(100, user.get('energy', 0) + 50)
        bot.send_message(user['id'], f"✅ Вы восстановили 50 энергии! Теперь у вас {user['energy']}% энергии.")

    elif item['id'] == 'medkit':
        user['HP'] = min(100, user.get('HP', 0) + 50)
        bot.send_message(user['id'], f"✅ Вы восстановили 50 HP! Теперь у вас {user['HP']}/100 HP.")

    elif item['id'] == 'student_card':
        if 'card' not in user['inventory']:
            user['inventory'].append('card')
        bot.send_message(user['id'], "✅ Вы купили карточку студента! Теперь вас пропускают в холле.")

    return True


def user_message(bot, message, user, location, all_users):
    if message == 'Пойти в школу!':
        transfer_user(user, 'yard')
    elif message == '🛒 Магазин Силаэдров':
        show_shop(bot, user)
    elif message == '💤 Отдохнуть (восстановить 50 энергии)':
        user['energy'] = min(100, user.get('energy', 0) + 50)
        bot.send_message(user['id'], f"✅ Вы отдохнули! Теперь у вас {user['energy']}% энергии.")
        user_enters_location(bot, user, location, all_users)
    elif message == '🔙 Назад':
        user_enters_location(bot, user, location, all_users)
    elif 'Силаэдров' in message:
        # Обработка покупки
        if process_purchase(bot, user, message):
            # Показываем обновленный магазин
            show_shop(bot, user)
    else:
        bot.send_message(user['id'], 'Я вас не понял')