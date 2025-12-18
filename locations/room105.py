from telebot import types
from methods import *
import random
import time
from datetime import datetime, timedelta


# В начало файла добавляем:
def can_throw_paper_at_inga(user):
    """Проверяет, можно ли кидаться бумагой в Ингу"""
    # Можно кидаться только если есть бумага и Инга присутствует
    if 'toilet_paper' not in user.get('inventory', []):
        return False, "У вас нет туалетной бумаги!"

    from locations.room105 import INGA_PRESENCE
    if not INGA_PRESENCE:
        return False, "Инги Александровны нет на месте!"

    return True, ""


def throw_paper_at_inga(bot, user):
    """Кидает бумагой в Ингу"""
    user['inventory'].remove('toilet_paper')

    # Шансы разных исходов
    outcome = random.randint(1, 10)

    if outcome <= 2:  # 20% шанс - попадание, но Инга рассмеялась
        bot.send_message(user['id'],
                         'Вы кинули туалетную бумагу в Ингу Александровну!\n'
                         'Инга рассмеялась: "Ох, какой шалун! Ладно, в этот раз прощаю."')
        return False  # Не отправляет в 105

    elif outcome <= 5:  # 30% шанс - попадание с последствиями
        bot.send_message(user['id'],
                         'Вы кинули туалетную бумагу в Ингу Александровну!\n'
                         'Инга в ярости: "Как ты смеешь! Быстро писать объяснительную!"')
        return True  # Отправляет в 105

    elif outcome <= 8:  # 30% шанс - промах
        bot.send_message(user['id'],
                         'Вы кинули туалетную бумагу, но промахнулись!\n'
                         'Инга: "Что это было? Всё равно в 105 на объяснительную!"')
        return True  # Отправляет в 105

    else:  # 20% шанс - критический промах
        bot.send_message(user['id'],
                         'Вы кинули туалетную бумагу, но она попала в вентилятор и разлетелась по всему кабинету!\n'
                         'Инга в бешенстве: "Ты уберёшь это всё! А потом в 105 на двойную объяснительную!"')
        user['ochota'] = 3  # Принудительная объяснительная
        return True  # Отправляет в 105

# Глобальные переменные для состояния Инги Александровны
INGA_PRESENCE = True
INGA_AWAY_UNTIL = None

# Глобальный код дружбы (обновляется ежедневно)
CURRENT_FRIENDSHIP_CODE = None
CODE_LAST_UPDATED = None

# Словарь для перевода эмоций
EMOTION_TRANSLATIONS = {
    "очень добро": "очень доброе",
    "добро": "доброе",
    "нейтрально": "нейтральное",
    "зло": "злое",
    "очень зло": "очень злое"
}

# Обратный словарь
REVERSE_EMOTION = {v: k for k, v in EMOTION_TRANSLATIONS.items()}

# Банк предложений для объяснительной (сгруппированные по тональности)
EXPLANATION_PHRASES = {
    "очень добро": [
        "Я искренне сожалею о своём поведении и обещаю исправиться",
        "Приношу свои глубочайшие извинения за допущенную ошибку",
        "Я осознал свою неправоту и обещаю больше так не поступать",
        "Прошу прощения за своё безответственное поведение",
        "Я полностью признаю свою вину и готов исправиться",
        "Сожалею о содеянном и обещаю впредь быть более ответственным",
        "Признаю свою ошибку и прошу дать шанс её исправить",
        "Я осознал, что был не прав, и обещаю измениться",
        "Прошу прощения за причинённые неудобства",
        "Я глубоко раскаиваюсь в своих действиях"
    ],
    "добро": [
        "Прошу прощения за своё поведение",
        "Я был не прав и обещаю исправиться",
        "Сожалею о случившемся",
        "Признаю свою ошибку",
        "Постараюсь больше так не делать",
        "Извините за мои действия",
        "Я неправильно поступил",
        "Обещаю быть внимательнее",
        "Приму меры, чтобы это не повторилось",
        "Я осознал свою неправоту"
    ],
    "нейтрально": [
        "Я был в кабинете и выполнил задание",
        "Ситуация произошла по техническим причинам",
        "Обстоятельства сложились таким образом",
        "Я действовал согласно инструкциям",
        "Это произошло в рабочем порядке",
        "Я находился на своём месте",
        "Всё происходило в рамках правил",
        "Я следовал установленному порядку",
        "Ситуация развивалась стандартно",
        "Я выполнял свои обязанности"
    ],
    "зло": [
        "Я не считаю себя виноватым",
        "Это была вынужденная мера",
        "Меня спровоцировали на это",
        "Я действовал в рамках самообороны",
        "Ситуация была не под моим контролем",
        "Меня неправильно поняли",
        "Это была ошибка системы",
        "Я не нарушал правила намеренно",
        "Обстоятельства вынудили меня так поступить",
        "Мою позицию неправильно интерпретировали"
    ],
    "очень зло": [
        "Я не собираюсь извиняться!",
        "Это ваша проблема, а не моя!",
        "Я сделал то, что считал нужным!",
        "Не вижу причин для объяснений!",
        "Мне всё равно на ваше мнение!",
        "Делайте что хотите!",
        "Я не признаю свою вину!",
        "Это абсурдные обвинения!",
        "Я не буду этого терпеть!",
        "У меня нет к вам претензий!"
    ]
}


def check_inga_status():
    """Проверяет, на месте ли Инга Александровна"""
    global INGA_PRESENCE, INGA_AWAY_UNTIL

    if INGA_AWAY_UNTIL and datetime.now() > INGA_AWAY_UNTIL:
        INGA_PRESENCE = True
        INGA_AWAY_UNTIL = None
    elif not INGA_PRESENCE and not INGA_AWAY_UNTIL:
        INGA_PRESENCE = True

    return INGA_PRESENCE


def inga_goes_away():
    """Инга уходит на время"""
    global INGA_PRESENCE, INGA_AWAY_UNTIL
    if INGA_PRESENCE:
        INGA_PRESENCE = False
        away_minutes = random.randint(1, 9)
        INGA_AWAY_UNTIL = datetime.now() + timedelta(minutes=away_minutes)
        return away_minutes
    return 0


def generate_friendship_code():
    """Генерирует новый код дружбы на сегодня"""
    global CURRENT_FRIENDSHIP_CODE, CODE_LAST_UPDATED

    emotions = ["очень добро", "добро", "нейтрально", "зло", "очень зло"]
    code = []

    # Генерируем 5 случайных эмоций (код дружбы)
    for _ in range(5):
        emotion = random.choice(emotions)
        code.append(emotion)

    CURRENT_FRIENDSHIP_CODE = code
    CODE_LAST_UPDATED = datetime.now().date()

    return code


def get_current_friendship_code():
    """Получает текущий код дружбы, обновляя его если нужно"""
    global CURRENT_FRIENDSHIP_CODE, CODE_LAST_UPDATED

    today = datetime.now().date()

    if CURRENT_FRIENDSHIP_CODE is None or CODE_LAST_UPDATED != today:
        generate_friendship_code()

    return CURRENT_FRIENDSHIP_CODE


def announce_friendship_code(bot, user):
    """Объявляет код дружбы на сегодня (только когда спрашивают отдельно)"""
    code = get_current_friendship_code()

    # Преобразуем эмоции в читаемый формат
    readable_code = [EMOTION_TRANSLATIONS.get(emotion, emotion) for emotion in code]

    code_text = ", ".join(readable_code)

    bot.send_message(user['id'],
                     f'Инга Александровна: "Я бы хотела бы сегодня увидеть в объяснительных: {code_text}"\n\n'
                     f'Запомни эту последовательность из 5 эмоций!')

    # После объявления возвращаемся в главное меню
    reset_to_main_menu(bot, user)


def start_explanation(bot, user):
    """Начинает процесс написания объяснительной"""
    user['explanation_step'] = 1
    user['explanation_selected_emotions'] = []
    user['explanation_selected_phrases'] = []

    # Показываем первое предложение
    show_explanation_step(bot, user)


def show_explanation_step(bot, user):
    """Показывает текущий шаг написания объяснительной"""
    step = user.get('explanation_step', 1)

    if step > 5:
        # Завершили написание объяснительной
        finish_explanation(bot, user)
        return

    # Генерируем варианты для текущего шага
    # 5 случайных предложений разных тональностей
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Собираем по одному предложению из каждой тональности
    emotions = ["очень добро", "добро", "нейтрально", "зло", "очень зло"]
    selected_phrases = []

    for emotion in emotions:
        phrases = EXPLANATION_PHRASES[emotion]
        selected_phrase = random.choice(phrases)
        selected_phrases.append({
            'text': selected_phrase,
            'emotion': emotion
        })

    # Перемешиваем варианты
    random.shuffle(selected_phrases)

    # Сохраняем варианты для этого шага
    user[f'step_{step}_options'] = selected_phrases

    # Добавляем кнопки
    for i, phrase_data in enumerate(selected_phrases):
        # Обрезаем длинные фразы для кнопки
        button_text = phrase_data['text']
        if len(button_text) > 40:
            button_text = button_text[:37] + "..."
        keyboard.add(types.KeyboardButton(button_text))

    bot.send_message(user['id'],
                     f'Шаг {step} из 5:\n'
                     f'Выберите предложение #{step} для объяснительной:',
                     reply_markup=keyboard)


def process_explanation_choice(bot, user, selected_text):
    """Обрабатывает выбор предложения для объяснительной"""
    step = user.get('explanation_step', 1)

    if step > 5:
        return

    # Находим выбранное предложение среди вариантов
    selected_option = None
    options = user.get(f'step_{step}_options', [])

    for option in options:
        # Сравниваем начало текста, так как на кнопке он мог быть обрезан
        if option['text'].startswith(selected_text[:30]):
            selected_option = option
            break

    if not selected_option:
        # Если точного совпадения нет, ищем по подстроке
        for option in options:
            if selected_text in option['text'] or option['text'] in selected_text:
                selected_option = option
                break

    if not selected_option:
        bot.send_message(user['id'], 'Не удалось распознать выбранное предложение. Попробуйте снова.')
        show_explanation_step(bot, user)
        return

    # Сохраняем выбор
    user['explanation_selected_emotions'].append(selected_option['emotion'])
    user['explanation_selected_phrases'].append(selected_option['text'])

    # Удаляем временные данные шага
    if f'step_{step}_options' in user:
        del user[f'step_{step}_options']

    # Переходим к следующему шагу
    user['explanation_step'] = step + 1

    if user['explanation_step'] > 5:
        finish_explanation(bot, user)
    else:
        show_explanation_step(bot, user)


def finish_explanation(bot, user):
    """Завершает написание объяснительной и проверяет код дружбы"""
    selected_emotions = user.get('explanation_selected_emotions', [])
    selected_phrases = user.get('explanation_selected_phrases', [])

    if len(selected_emotions) != 5 or len(selected_phrases) != 5:
        bot.send_message(user['id'], 'Ошибка: объяснительная неполная')
        reset_to_main_menu(bot, user)
        return

    # Получаем код дружбы на сегодня
    friendship_code = get_current_friendship_code()

    # Сравниваем эмоции выбранных предложений с кодом дружбы
    matches = 0
    result_text = "Ваша объяснительная:\n\n"

    for i in range(5):
        user_emotion = selected_emotions[i]
        correct_emotion = friendship_code[i]
        is_match = user_emotion == correct_emotion

        result_text += f"{i + 1}. {selected_phrases[i]}\n"
        result_text += f"   (Тональность: {EMOTION_TRANSLATIONS.get(user_emotion, user_emotion)})\n"

        if is_match:
            matches += 1
            result_text += "   ✅ Совпадает с кодом дружбы!\n"
        else:
            result_text += f"   ❌ Должно быть: {EMOTION_TRANSLATIONS.get(correct_emotion, correct_emotion)}\n"

        result_text += "\n"

    # Проверяем, полностью ли совпал код
    if matches == 5:
        # Полностью угадали код - объяснительная не засчитывается
        result_text += "\n🎉 Инга Александровна: 'Поздравляю! Ты полностью угадал мой код дружбы! Объяснительная не нужна!'"

        # Награда за угаданный код
        user['silаedry'] = user.get('silаedry', 0) + 20
        user['experience'] = user.get('experience', 0) + 10

        # Обновляем статистику кодов дружбы
        update_friendship_stats(user, True, True)

        # Очищаем цель объяснительной
        user['ochota'] = 1

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Выйти"))

        bot.send_message(user['id'], result_text, reply_markup=keyboard)

        # Очищаем состояние
        cleanup_explanation_state(user)
    else:
        # Не угадали код - объяснительная засчитывается
        result_text += f"\nВы угадали {matches}/5 тональностей.\n"
        result_text += "Инга Александровна: 'Объяснительная принята.'"

        # Сохраняем объяснительную
        save_explanation(user, selected_phrases, selected_emotions)

        # Обновляем статистику кодов дружбы
        update_friendship_stats(user, False, True)

        # Очищаем цель объяснительной
        user['ochota'] = 1

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Выйти"))

        bot.send_message(user['id'], result_text, reply_markup=keyboard)

        # Очищаем состояние
        cleanup_explanation_state(user)


def save_explanation(user, phrases, emotions):
    """Сохраняет объяснительную в профиль пользователя"""
    full_text = " ".join(phrases)

    if 'obiyasnitelnay' not in user:
        user['obiyasnitelnay'] = []

    explanation_data = {
        'text': full_text,
        'emotions': emotions,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user['obiyasnitelnay'].append(explanation_data)
    user['obiyasnitelinee'] = user.get('obiyasnitelinee', 0) + 1


def update_friendship_stats(user, is_correct, during_explanation=False):
    """Обновляет статистику кодов дружбы пользователя"""
    if 'friendship_stats' not in user:
        user['friendship_stats'] = {
            'total_attempts': 0,
            'correct_attempts': 0,
            'consecutive_correct': 0,
            'consecutive_wrong': 0,
            'last_attempt_date': None,
            'during_explanation_correct': 0,
            'during_explanation_wrong': 0
        }

    stats = user['friendship_stats']
    stats['total_attempts'] += 1
    stats['last_attempt_date'] = datetime.now().strftime("%Y-%m-%d")

    if is_correct:
        stats['correct_attempts'] += 1
        stats['consecutive_correct'] += 1
        stats['consecutive_wrong'] = 0

        if during_explanation:
            stats['during_explanation_correct'] += 1
            # Проверяем, стал ли пользователь любимчиком
            if stats['during_explanation_correct'] >= 3:
                if 'ingas_favorite' not in user['inventory']:
                    user['inventory'].append('ingas_favorite')
                    user['became_favorite_date'] = datetime.now().strftime("%Y-%m-%d")
                    bot.send_message(user['id'],
                                     "\n\n🎉 Инга Александровна: 'Ты три раза подряд угадал код во время объяснительной! Ты теперь мой любимчик!'")
    else:
        stats['consecutive_wrong'] += 1
        stats['consecutive_correct'] = 0

        if during_explanation:
            stats['during_explanation_wrong'] += 1
            # Проверяем, не потерял ли статус любимчика
            if 'ingas_favorite' in user['inventory']:
                if stats['during_explanation_wrong'] >= 2:
                    user['inventory'].remove('ingas_favorite')
                    if 'became_favorite_date' in user:
                        del user['became_favorite_date']
                    # Сбрасываем счетчики
                    stats['during_explanation_correct'] = 0
                    stats['during_explanation_wrong'] = 0
                    bot.send_message(user['id'],
                                     "\n\n😞 Инга Александровна: 'Ты два раза подряд не угадал код... Ты больше не мой любимчик.'")


def cleanup_explanation_state(user):
    """Очищает состояние написания объяснительной"""
    keys_to_remove = []
    for key in user.keys():
        if key.startswith('explanation_') or key.startswith('step_'):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del user[key]


def reset_to_main_menu(bot, user):
    """Сбрасывает состояние и возвращает к главному меню"""
    cleanup_explanation_state(user)
    user_enters_location(bot, user, None, [])


def show_inga_favorite_menu(bot, user):
    """Показывает меню для любимчика Инги"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Особый чай от Инги"))
    keyboard.add(types.KeyboardButton(text="Лучшие сушки"))
    keyboard.add(types.KeyboardButton(text="Избавить от объяснительной"))
    keyboard.add(types.KeyboardButton(text="Помочь с документами"))
    keyboard.add(types.KeyboardButton(text="Выйти"))

    bot.send_message(user['id'],
                     'Инга Александровна: "Что нужно, мой любимчик?"',
                     reply_markup=keyboard)


def handle_inga_favorite_choice(bot, user, message):
    """Обрабатывает выбор в меню любимчика Инги"""
    if message == "Особый чай от Инги":
        user['energy'] = min(100, user.get('energy', 0) + 40)
        user['water'] = min(100, user.get('water', 0) + 40)
        bot.send_message(user['id'],
                         'Инга наливает вам свой фирменный чай. +40 энергии, +40 воды!')

    elif message == "Лучшие сушки":
        user['food'] = min(100, user.get('food', 0) + 30)
        user['experience'] = user.get('experience', 0) + 10
        bot.send_message(user['id'],
                         'Инга достает для вас лучшие сушки. +30 сытости, +10 опыта!')

    elif message == "Избавить от объяснительной":
        # Сбрасываем цель объяснительной
        if user.get('ochota') in [2, 3]:
            user['ochota'] = 1
            user['experience'] = max(0, user.get('experience', 0) - 5)
            bot.send_message(user['id'],
                             'Инга порвала вашу объяснительную: "Для любимчика делаю исключение!"\n-5 опыта')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'], 'Вы можете идти.', reply_markup=keyboard)

    elif message == "Помочь с документами":
        user['experience'] = user.get('experience', 0) + 15
        bot.send_message(user['id'],
                         'Вы помогли Инге разобрать документы. +15 опыта!')

    elif message == "Выйти":
        transfer_user(user, 'hall')


def user_enters_location(bot, user, location, all_users):
    check_inga_status()

    # Очищаем любые временные состояния при входе
    cleanup_explanation_state(user)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Проверяем, любимчик ли Инги
    if 'ingas_favorite' in user.get('inventory', []):
        show_inga_favorite_menu(bot, user)
        return

    # Проверяем предметы для использования
    if 'fake_alarm' in user.get('inventory', []):
        keyboard.add(types.KeyboardButton(text="🚨 Использовать фейк-сигнализацию"))

    if 'explanation_cancel' in user.get('inventory', []):
        keyboard.add(types.KeyboardButton(text="📝 Использовать отмену объяснительной"))

    # Проверяем цель прихода
    ochota = user.get('ochota', 1)

    if ochota == 0:
        if INGA_PRESENCE:
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Карточку взять"))
            keyboard.add(types.KeyboardButton(text="Сушки попросить"))
            keyboard.add(types.KeyboardButton(text="Ударить Ингу"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'],
                             'Инга Александровна: "Ну что тебе нужно, студент?"',
                             reply_markup=keyboard)
        else:
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Карточку взять"))
            keyboard.add(types.KeyboardButton(text="Сушки взять"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'],
                             'Инги Александровны нет на месте! Можно действовать свободно.',
                             reply_markup=keyboard)

    elif ochota == 1:
        if INGA_PRESENCE:
            if random.randint(1, 2) == 1:
                bot.send_message(user['id'],
                                 'Инга Александровна: "Опять ты тут?! Садись писать объяснительную!"')
                user['ochota'] = 2
                start_explanation(bot, user)
                return
            else:
                keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
                keyboard.add(types.KeyboardButton(text="Выйти"))
                bot.send_message(user['id'],
                                 'Инга Александровна: "Уходи отсюда, не мешай работать!"',
                                 reply_markup=keyboard)
        else:
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Сушки взять"))
            keyboard.add(types.KeyboardButton(text="Просто посидеть"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'],
                             'Инги Александровны нет! Можно расслабиться.',
                             reply_markup=keyboard)

    elif ochota == 2:
        # Прямо начинаем писать объяснительную
        start_explanation(bot, user)
        return

    elif ochota == 3:
        bot.send_message(user['id'],
                         'Инга Александровна: "Ты думал, убежишь?! Садись и пиши объяснительную!"')
        start_explanation(bot, user)
        return

    bot.send_message(user['id'], 'Что выберете?', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете 105')


def user_message(bot, message, user, location, all_users):
    check_inga_status()

    # Всегда обрабатываем выход первым
    if message == "Выйти" or message == "Переход: холл 1 этажа":
        transfer_user(user, 'hall')
        return

    # Проверяем, является ли пользователь любимчиком Инги
    if 'ingas_favorite' in user.get('inventory', []):
        handle_inga_favorite_choice(bot, user, message)
        return

    # Обработка использования предметов
    if message == "🚨 Использовать фейк-сигнализацию":
        if 'fake_alarm' in user.get('inventory', []):
            user['inventory'].remove('fake_alarm')
            # Активируем эффект - Инга уходит на 10 минут
            away_minutes = inga_goes_away()
            bot.send_message(user['id'],
                             f"🚨 Сработала фейк-сигнализация! Инга Александровна вышла на {away_minutes} минут.")
            reset_to_main_menu(bot, user)
        else:
            reset_to_main_menu(bot, user)
        return

    elif message == "📝 Использовать отмену объяснительной":
        if 'explanation_cancel' in user.get('inventory', []):
            user['inventory'].remove('explanation_cancel')
            if user.get('ochota') in [2, 3]:
                user['ochota'] = 1
                bot.send_message(user['id'],
                                 "✅ Объяснительная отменена! Инга Александровна: 'Ладно, в этот раз прощаю.'")
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Выйти"))
                bot.send_message(user['id'], 'Вы можете идти.', reply_markup=keyboard)
            else:
                bot.send_message(user['id'], "У вас нет активной объяснительной для отмены.")
                reset_to_main_menu(bot, user)
        else:
            reset_to_main_menu(bot, user)
        return

    # Обработка кода дружбы (только когда спрашивают отдельно)
    if message == "Спросить код дружбы":
        if user.get('ochota') in [2, 3]:
            bot.send_message(user['id'], 'Инга Александровна: "Сначала разберись с объяснительной!"')
            reset_to_main_menu(bot, user)
        else:
            announce_friendship_code(bot, user)
        return

    # Проверяем, находится ли пользователь в процессе написания объяснительной
    if user.get('explanation_step') is not None and user.get('explanation_step') <= 5:
        # Это выбор предложения для объяснительной
        process_explanation_choice(bot, user, message)
        return

    # Проверяем цель прихода
    ochota = user.get('ochota', 1)

    # Обработка для ochota = 0 (пришел за карточкой/по делу)
    if ochota == 0:
        if INGA_PRESENCE:
            if message == "Чайку попить":
                if random.randint(1, 2) == 1:
                    user['energy'] = min(100, user.get('energy', 0) + 10)
                    user['water'] = min(100, user.get('water', 0) + 20)
                    bot.send_message(user['id'],
                                     'Инга Александровна: "На, попей чайку."\nВы попили чай. +10 энергии, +20 воды.')
                    reset_to_main_menu(bot, user)
                else:
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Какой еще чай?! Садись писать объяснительную!"')
                    user['ochota'] = 2
                    start_explanation(bot, user)
                return

            elif message == "Карточку взять":
                if 'card' not in user['inventory']:
                    user['inventory'].append('card')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Чайку попить"))
                keyboard.add(types.KeyboardButton(text="Выйти"))
                bot.send_message(user['id'],
                                 'Инга Александровна: "На, держи свою карточку."\nКарточка добавлена в инвентарь.',
                                 reply_markup=keyboard)
                return

            elif message == "Сушки попросить":
                if random.randint(1, 3) == 1:
                    user['food'] = min(100, user.get('food', 0) + 15)
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Возьми сушки."\nВы съели сушки. +15 сытости.')
                    reset_to_main_menu(bot, user)
                else:
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Сушки?! Ты еще и есть хочешь?! Объяснительную пиши!"')
                    user['ochota'] = 2
                    start_explanation(bot, user)
                return

            elif message == "Ударить Ингу":
                bot.send_message(user['id'],
                                 'Вы попытались ударить Ингу Александровну, но она оказалась быстрее!\n'
                                 '"В 105 на объяснительную!"')
                user['ochota'] = 2
                start_explanation(bot, user)
                return

        else:
            # Инги нет
            if message == "Чайку попить":
                user['energy'] = min(100, user.get('energy', 0) + 10)
                user['water'] = min(100, user.get('water', 0) + 20)
                bot.send_message(user['id'], 'Вы попили чай. +10 энергии, +20 воды.')
                reset_to_main_menu(bot, user)
                return

            elif message == "Карточку взять":
                if 'card' not in user['inventory']:
                    user['inventory'].append('card')
                bot.send_message(user['id'], 'Вы взяли карточку со стола.')
                reset_to_main_menu(bot, user)
                return

            elif message == "Сушки взять":
                user['food'] = min(100, user.get('food', 0) + 15)
                bot.send_message(user['id'], 'Вы взяли сушки. +15 сытости.')
                reset_to_main_menu(bot, user)
                return

    # Обработка для ochota = 1 (просто пришел)
    elif ochota == 1:
        if INGA_PRESENCE:
            # Если Инга на месте и мы получили непонятное сообщение, показываем меню
            reset_to_main_menu(bot, user)
        else:
            # Инги нет
            if message == "Чайку попить":
                user['energy'] = min(100, user.get('energy', 0) + 10)
                user['water'] = min(100, user.get('water', 0) + 20)
                bot.send_message(user['id'], 'Вы попили чай. +10 энергии, +20 воды.')
                reset_to_main_menu(bot, user)
                return

            elif message == "Сушки взять":
                user['food'] = min(100, user.get('food', 0) + 15)
                bot.send_message(user['id'], 'Вы взяли сушки. +15 сытости.')
                reset_to_main_menu(bot, user)
                return

            elif message == "Просто посидеть":
                user['energy'] = min(100, user.get('energy', 0) + 5)
                bot.send_message(user['id'], 'Вы посидели в тишине. +5 энергии.')
                reset_to_main_menu(bot, user)
                return

    # Если ни одно из условий не сработало, сбрасываем к главному меню
    reset_to_main_menu(bot, user)


def run_events(bot, location, all_users):
    """Ежедневная генерация нового кода дружбы в 00:00"""
    global CURRENT_FRIENDSHIP_CODE, CODE_LAST_UPDATED

    now = datetime.now()

    # Если сейчас около 00:00 и код еще не обновлялся сегодня
    if now.hour == 0 and now.minute < 5:
        if CODE_LAST_UPDATED != now.date():
            generate_friendship_code()

    check_inga_status()