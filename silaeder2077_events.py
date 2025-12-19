import time
from datetime import datetime, timedelta
import random
from methods import *
from library import users, locations
import json

# Словарь для отслеживания беглецов
escapees = {}


def common_events(bot, user):
    """Общие события для всех игроков"""
    now = datetime.now()

    # Проверяем, не находится ли игрок в бессознательном состоянии
    if user.get('unconscious_until'):
        try:
            unconscious_until = datetime.fromisoformat(user['unconscious_until'])
            if now < unconscious_until:
                # Игрок все еще без сознания
                time_left = (unconscious_until - now).total_seconds() / 60
                if time_left < 1:
                    time_display = f"{int(time_left * 60)} секунд"
                else:
                    time_display = f"{int(time_left)} минут"

                # Каждые 5 минут отправляем сообщение о состоянии
                last_notify = user.get('last_unconscious_notify')
                if not last_notify or (now - datetime.fromisoformat(last_notify)).total_seconds() > 300:
                    bot.send_message(user['id'],
                                     f"💤 Вы все еще без сознания... Осталось {time_display}")
                    user['last_unconscious_notify'] = now.isoformat()
                return
            else:
                # Игрок пришел в сознание
                user['HP'] = 100
                user['energy'] = 100
                user['food'] = 100
                user['water'] = 100
                user['unconscious_until'] = None
                if 'last_unconscious_notify' in user:
                    del user['last_unconscious_notify']

                bot.send_message(user['id'],
                                 "✨ Вы пришли в сознание! Все характеристики восстановлены до 100%!")

                # Автоматически перемещаем в дом
                if user.get('location') != 'home':
                    transfer_user(user, 'home')
        except:
            # Если ошибка в формате времени, сбрасываем состояние
            user['unconscious_until'] = None

    # Обновляем время последней активности
    user['last_activity'] = now.isoformat()

    # Только если игрок не дома
    if user.get('location') != 'home':
        # Каждые 10 минут теряем 1 еду и 1 воду
        last_activity = datetime.fromisoformat(user.get('last_activity', now.isoformat()))
        if (now - last_activity).total_seconds() > 600:  # 10 минут
            user['food'] = max(0, user.get('food', 100) - 1)
            user['water'] = max(0, user.get('water', 100) - 1)
            user['last_activity'] = now.isoformat()

    # Каждую минуту восстанавливаем 1 энергию (если не без сознания)
    user['energy'] = min(100, user.get('energy', 100) + 1)

    # Проверяем базовые потребности
    check_basic_needs(bot, user)

    # Проверяем беглецов
    if user['id'] in escapees:
        chance = escapees[user['id']]['chance']
        if random.randint(1, 100) <= chance:
            bot.send_message(user['id'],
                             'Инга Александровна нашла вас! "А ну быстро в 105 писать объяснительную!"')
            user['ochota'] = 3
            transfer_user_with_goal(user, 'room105', 'force')
            del escapees[user['id']]
        else:
            escapees[user['id']]['chance'] = min(100, chance + 5)


def check_basic_needs(bot, user):
    """Проверяет базовые потребности и наносит урон HP если нужно"""
    hp_loss = 0

    # Проверяем каждую характеристику
    if user.get('energy', 100) <= 0:
        hp_loss += 1
        # Восстанавливаем немного энергии чтобы не терять HP постоянно
        user['energy'] = 1

    if user.get('food', 100) <= 0:
        hp_loss += 1
        user['food'] = 1

    if user.get('water', 100) <= 0:
        hp_loss += 1
        user['water'] = 1

    # Наносим урон HP
    if hp_loss > 0:
        current_hp = user.get('HP', 100)
        new_hp = max(0, current_hp - hp_loss)
        user['HP'] = new_hp

        # Если HP упало до 0, игрок теряет сознание
        if new_hp <= 0:
            make_unconscious(bot, user)
        elif new_hp <= 20:
            # Предупреждение при низком HP
            bot.send_message(user['id'],
                             f"⚠️ Внимание! У вас критически низкий уровень HP: {new_hp}/100. "
                             f"Поешьте, попейте и отдохните!")

    # Восстанавливаем HP если все характеристики в норме
    elif user.get('HP', 100) < 100:
        if (user.get('energy', 0) >= 80 and
                user.get('food', 0) >= 80 and
                user.get('water', 0) >= 80):
            user['HP'] = min(100, user.get('HP', 100) + 1)


def make_unconscious(bot, user):
    """Отправляет игрока в бессознательное состояние"""
    unconscious_time = 60  # 60 минут = 1 час
    unconscious_until = datetime.now() + timedelta(minutes=unconscious_time)

    user['unconscious_until'] = unconscious_until.isoformat()
    user['HP'] = 0

    # Отправляем сообщение
    bot.send_message(user['id'],
                     f"💤 Вы потеряли сознание из-за истощения! "
                     f"Вы будете без сознания 1 час. "
                     f"После пробуждения все характеристики будут восстановлены.")

    # Автоматически перемещаем в дом
    if user.get('location') != 'home':
        transfer_user(user, 'home')


def handle_escape(user_id, chance=75):
    """Регистрирует игрока как беглеца от объяснительной"""
    escapees[user_id] = {
        'chance': chance,
        'start_time': datetime.now()
    }


def check_escapes():
    """Проверяет и удаляет старые записи о беглецах"""
    current_time = datetime.now()
    to_remove = []

    for user_id, data in escapees.items():
        if current_time - data['start_time'] > timedelta(hours=24):
            to_remove.append(user_id)

    for user_id in to_remove:
        del escapees[user_id]


def room105_events(bot, location, all_users):
    """События для комнаты 105"""
    from locations.room105 import check_inga_status, inga_goes_away

    current_time = time.time()
    if not hasattr(room105_events, 'last_check'):
        room105_events.last_check = current_time

    if current_time - room105_events.last_check >= 600:
        room105_events.last_check = current_time

        if random.randint(1, 10) == 1:
            away_minutes = inga_goes_away()
            for user in all_users:
                bot.send_message(user['id'],
                                 f'Инга Александровна: "Мне нужно отлучиться на {away_minutes} минут. Ведите себя прилично!"')

        check_inga_status()


def save_game_state():
    """Сохраняет состояние игры"""
    try:
        from library import save_state_to_file, users, locations
        save_state_to_file(users, locations)
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")


while True:
    check_escapes()

    for user in users:
        try:
            common_events(bot, user)
        except Exception as e:
            print(f"Ошибка в common_events для пользователя {user.get('id')}: {e}")

    for location in locations:
        location_users = get_location_users(location['id'])

        if location['id'] == 'room105':
            try:
                room105_events(bot, location, location_users)
            except Exception as e:
                print(f"Ошибка в событиях room105: {e}")
        else:
            try:
                modules[location['id']].run_events(bot, location, location_users)
            except Exception as e:
                pass

    # Сохраняем состояние каждую минуту
    save_game_state()

    time.sleep(60)