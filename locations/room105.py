from telebot import types
from methods import *
import random
import time
from datetime import datetime, timedelta

# Глобальные переменные для состояния Инги Александровны
INGA_PRESENCE = True
INGA_AWAY_UNTIL = None

# Глобальный код дружбы (обновляется ежедневно)
CURRENT_FRIENDSHIP_CODE = None
CODE_LAST_UPDATED = None

# Банк фраз для кода дружбы
FRIENDSHIP_PHRASES_POOL = [
    # Очень добрые (10)
    "Я вас очень уважаю и ценю",
    "Вы прекрасный человек, с вами приятно общаться",
    "Мне так приятно видеть вас здесь",
    "Я восхищаюсь вашим характером",
    "Вы всегда так внимательны и добры",
    "Ваше присутствие скрашивает мой день",
    "Я всегда рад вас видеть",
    "Вы заслуживаете только самого лучшего",
    "Мне очень повезло знать вас",
    "Вы вдохновляете меня на хорошие поступки",

    # Добрые (15)
    "Спасибо за вашу помощь",
    "Вы хороший человек",
    "Мне нравится с вами работать",
    "Вы всегда вежливы и учтивы",
    "Приятно видеть вас в хорошем настроении",
    "Вы правильно поступили",
    "Я ценю ваше мнение",
    "Вы проявляете заботу о других",
    "Ваши слова мне приятны",
    "Вы достойный человек",
    "Спасибо за понимание",
    "Вы хорошо справляетесь",
    "Мне приятно наше общение",
    "Вы заслуживаете уважения",
    "Я доволен вашими действиями",

    # Нейтральные (15)
    "Всё в порядке, как обычно",
    "Как ваши дела сегодня?",
    "Что нового произошло?",
    "Погода сегодня вполне сносная",
    "Всё идёт по установленному плану",
    "Ситуация развивается стандартно",
    "Ничего особенного не происходит",
    "Всё как всегда, без изменений",
    "Рабочий процесс идёт нормально",
    "Стандартная рутина дня",
    "Вопрос решается обычным способом",
    "Никаких эксцессов не наблюдается",
    "Всё в рамках допустимого",
    "Процесс протекает типично",
    "Ситуация под контролем",

    # Злые (15)
    "Вы меня разочаровали своим поведением",
    "Я недоволен вашими действиями",
    "Такое поведение неприемлемо",
    "Вы совершили серьёзную ошибку",
    "Меня это искренне злит",
    "Вы поступили неправильно",
    "Я ожидал от вас большего",
    "Это возмутительно с вашей стороны",
    "Вы нарушили правила",
    "Меня не устраивает ваша позиция",
    "Вы проявили неуважение",
    "Это недопустимо в нашей ситуации",
    "Вы подвели мои ожидания",
    "Ваши слова меня огорчили",
    "Вы поступили необдуманно",

    # Очень злые (10)
    "Я вас искренне ненавижу!",
    "Убирайтесь отсюда немедленно!",
    "Вы ужасный человек!",
    "Больше никогда так не делайте!",
    "Мне противно с вами общаться!",
    "Вы безнадёжны в своих поступках!",
    "Я не хочу вас больше видеть!",
    "Вы вызываете у меня отвращение!",
    "Проваливайте и не возвращайтесь!",
    "Вы самый неприятный человек из всех, кого я знаю!"
]

# Эмоциональные категории для каждой фразы
PHRASE_EMOTIONS = {}
for i, phrase in enumerate(FRIENDSHIP_PHRASES_POOL):
    if i < 10:
        PHRASE_EMOTIONS[phrase] = "очень добро"
    elif i < 25:
        PHRASE_EMOTIONS[phrase] = "добро"
    elif i < 40:
        PHRASE_EMOTIONS[phrase] = "нейтрально"
    elif i < 55:
        PHRASE_EMOTIONS[phrase] = "зло"
    else:
        PHRASE_EMOTIONS[phrase] = "очень зло"


# Загрузка текстов объяснительных
def load_explanation_texts():
    texts = {}
    emotion_types = ['very_good', 'good', 'neutral', 'bad', 'very_bad']

    for emotion in emotion_types:
        texts[emotion] = {}
        for i in range(1, 5):
            filename = f'texts/explanation/{emotion}_{i}.txt'
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                    texts[emotion][i] = lines
            except:
                texts[emotion][i] = [f"{emotion} предложение {j}" for j in range(1, 51)]

    return texts


EXPLANATION_TEXTS = load_explanation_texts()


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

    # Генерируем 4 случайные эмоции
    for _ in range(4):
        emotion = random.choice(emotions)

        # Выбираем случайную фразу с нужной эмоцией
        possible_phrases = [p for p, e in PHRASE_EMOTIONS.items() if e == emotion]
        if not possible_phrases:
            possible_phrases = ["Нет подходящей фразы"]

        phrase = random.choice(possible_phrases)

        # Генерируем варианты: 1 правильный + 4 неправильных
        options = generate_options(phrase, emotion)

        code.append({
            "emotion": emotion,
            "phrase": phrase,
            "options": options
        })

    CURRENT_FRIENDSHIP_CODE = code
    CODE_LAST_UPDATED = datetime.now().date()
    return code


def generate_options(correct_phrase, correct_emotion):
    """Генерирует 5 вариантов фраз (1 правильная + 4 случайных)"""
    all_phrases = list(FRIENDSHIP_PHRASES_POOL)

    # Убираем правильную фразу из списка
    if correct_phrase in all_phrases:
        all_phrases.remove(correct_phrase)

    # Выбираем 4 случайные неправильные фразы
    selected_wrong = random.sample(all_phrases, 4)

    # Собираем все варианты
    all_options = [correct_phrase] + selected_wrong

    # Перемешиваем
    random.shuffle(all_options)

    return all_options


def get_current_friendship_code():
    """Получает текущий код дружбы, обновляя его если нужно"""
    global CURRENT_FRIENDSHIP_CODE, CODE_LAST_UPDATED

    today = datetime.now().date()

    if CURRENT_FRIENDSHIP_CODE is None or CODE_LAST_UPDATED != today:
        generate_friendship_code()

    return CURRENT_FRIENDSHIP_CODE


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
                    return True  # Стал любимчиком
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
                    return False  # Потерял статус

    return None  # Ничего не изменилось


def start_friendship_code(bot, user, during_explanation=False):
    """Начинает ввод кода дружбы"""
    code = get_current_friendship_code()

    user['friendship_step'] = 0
    user['friendship_input'] = []
    user['friendship_during_explanation'] = during_explanation

    # Показываем первый шаг
    show_friendship_step(bot, user, code)


def show_friendship_step(bot, user, code):
    """Показывает текущий шаг кода дружбы"""
    step = user['friendship_step']

    if step >= 4:
        # Завершили ввод
        check_friendship_code(bot, user, code)
        return

    current_step = code[step]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Добавляем варианты ответов (5 фраз)
    for option in current_step['options']:
        keyboard.add(types.KeyboardButton(option))

    context = ""
    if user.get('friendship_during_explanation'):
        context = "\n\nИнга Александровна: 'Я добавлю это в твою объяснительную...'"

    bot.send_message(user['id'],
                     f'Шаг {step + 1} из 4:\n\n'
                     f'"{current_step["phrase"]}"\n\n'
                     f'Какая это фраза? Выберите идентичную фразу из вариантов:{context}',
                     reply_markup=keyboard)


def process_friendship_input(bot, user, selected_phrase):
    """Обрабатывает выбор игрока в коде дружбы"""
    if 'friendship_step' not in user:
        return

    code = get_current_friendship_code()
    step = user['friendship_step']

    if step >= 4:
        return

    current_step = code[step]

    # Проверяем, правильно ли выбрана фраза
    is_correct = selected_phrase == current_step['phrase']

    user['friendship_input'].append({
        'phrase': selected_phrase,
        'correct_phrase': current_step['phrase'],
        'emotion': PHRASE_EMOTIONS.get(selected_phrase, "неизвестно"),
        'correct_emotion': current_step['emotion'],
        'is_correct': is_correct
    })
    user['friendship_step'] += 1

    # Показываем следующий шаг или проверяем результат
    show_friendship_step(bot, user, code)


def check_friendship_code(bot, user, code):
    """Проверяет весь введенный код"""
    correct_count = 0
    results = []

    for i, user_input in enumerate(user['friendship_input']):
        if user_input['is_correct']:
            correct_count += 1

        results.append({
            'step': i + 1,
            'phrase': code[i]['phrase'],
            'user_choice': user_input['phrase'],
            'is_correct': user_input['is_correct']
        })

    during_explanation = user.get('friendship_during_explanation', False)

    # Обновляем статистику
    status_change = update_friendship_stats(user, correct_count == 4, during_explanation)

    # Формируем результат
    if during_explanation:
        if correct_count == 4:
            result_message = "✅ Инга Александровна: 'Правильно! Это пойдет в твою пользу.'\n"
        else:
            result_message = f"❌ Инга Александровна: 'Неправильно! {correct_count}/4. Это ухудшит твое положение.'\n"
    else:
        if correct_count == 4:
            result_message = "✅ Инга Александровна: 'Поздравляю! Ты угадал код!'"
        else:
            result_message = f"❌ Инга Александровна: 'Не угадал... {correct_count}/4. Попробуй завтра снова!'"

    # Показываем детали
    result_message += f"\n\nРезультат: {correct_count}/4 правильных"

    for result in results:
        status = "✅" if result['is_correct'] else "❌"
        result_message += f"\n{status} Шаг {result['step']}: "
        if not result['is_correct']:
            result_message += f"\n   Правильно: '{result['phrase']}'"
            result_message += f"\n   Вы выбрали: '{result['user_choice']}'"

    # Обработка изменения статуса любимчика
    if status_change is True:
        result_message += "\n\n🎉 Инга Александровна: 'Ты три раза подряд угадал код во время объяснительной! Ты теперь мой любимчик!'"

        # Награда за статус любимчика
        user['experience'] = user.get('experience', 0) + 50
        user['energy'] = min(100, user.get('energy', 0) + 30)

        # Показываем меню любимчика
        show_inga_favorite_menu(bot, user)
    elif status_change is False:
        result_message += "\n\n😞 Инга Александровна: 'Ты два раза подряд не угадал код... Ты больше не мой любимчик.'"

        # Штраф за потерю статуса
        user['energy'] = max(0, user.get('energy', 0) - 20)

        # Возвращаем к обычному меню
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if during_explanation:
            keyboard.add(types.KeyboardButton("Продолжить объяснительную"))
        else:
            keyboard.add(types.KeyboardButton("📋 Общее меню"))
        bot.send_message(user['id'], result_message, reply_markup=keyboard)
    else:
        # Ничего не изменилось
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if during_explanation:
            keyboard.add(types.KeyboardButton("Продолжить объяснительную"))
        else:
            keyboard.add(types.KeyboardButton("📋 Общее меню"))
        bot.send_message(user['id'], result_message, reply_markup=keyboard)

    # Очищаем данные кода
    if 'friendship_step' in user:
        del user['friendship_step']
    if 'friendship_input' in user:
        del user['friendship_input']
    if 'friendship_during_explanation' in user:
        del user['friendship_during_explanation']


def show_inga_favorite_menu(bot, user):
    """Показывает меню для любимчика Инги"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Особый чай от Инги"))
    keyboard.add(types.KeyboardButton("Лучшие сушки"))
    keyboard.add(types.KeyboardButton("Избавить от объяснительной"))
    keyboard.add(types.KeyboardButton("Помочь с документами"))
    keyboard.add(types.KeyboardButton("Выйти"))

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
        if user.get('ochota') == 2 or user.get('ochota') == 3:
            user['ochota'] = 1
            user['experience'] = max(0, user.get('experience', 0) - 5)  # Небольшой штраф
            bot.send_message(user['id'],
                             'Инга порвала вашу объяснительную: "Для любимчика делаю исключение!"\n-5 опыта')

    elif message == "Помочь с документами":
        user['experience'] = user.get('experience', 0) + 15
        bot.send_message(user['id'],
                         'Вы помогли Инге разобрать документы. +15 опыта!')

    elif message == "Выйти":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Переход: холл"))
        bot.send_message(user['id'], 'Вы вышли из кабинета.', reply_markup=keyboard)


def start_explanation(bot, user):
    """Начинает процесс написания объяснительной"""
    user['explanation_step'] = 1
    user['explanation_text'] = []
    user['explanation_emotion'] = None

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Очень добрый тон"))
    keyboard.add(types.KeyboardButton(text="Добрый тон"))
    keyboard.add(types.KeyboardButton(text="Нейтральный тон"))
    keyboard.add(types.KeyboardButton(text="Злой тон"))
    keyboard.add(types.KeyboardButton(text="Очень злой тон"))

    bot.send_message(user['id'],
                     'Выберите эмоциональный тон для начала объяснительной:',
                     reply_markup=keyboard)


def start_explanation_with_friendship(bot, user):
    """Начинает объяснительную с возможностью ввода кода дружбы"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Начать писать объяснительную"))
    keyboard.add(types.KeyboardButton(text="Попробовать код дружбы"))

    bot.send_message(user['id'],
                     'Инга Александровна: "Ты здесь за объяснительной. Можешь начать писать или...\n'
                     'Попробуешь угадать мой код дружбы? Если угадаешь - учту это в твою пользу."',
                     reply_markup=keyboard)


def continue_explanation(bot, user, emotion_choice):
    """Продолжает написание объяснительной"""
    emotion_map = {
        "Очень добрый тон": "very_good",
        "Добрый тон": "good",
        "Нейтральный тон": "neutral",
        "Злой тон": "bad",
        "Очень злой тон": "very_bad"
    }

    emotion = emotion_map.get(emotion_choice, "neutral")
    user['explanation_emotion'] = emotion

    # Выбираем случайное предложение для текущего шага
    step = user['explanation_step']
    if step <= 4:
        options = EXPLANATION_TEXTS[emotion][step]
        selected = random.choice(options)
        user['explanation_text'].append(selected)

        bot.send_message(user['id'], f'Предложение {step}: {selected}')

        if step == 4:
            # Завершаем объяснительную
            complete_explanation(bot, user)
        else:
            user['explanation_step'] += 1

            # Предлагаем варианты для следующего предложения
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for emotion_opt in emotion_map.keys():
                keyboard.add(types.KeyboardButton(text=emotion_opt))

            bot.send_message(user['id'],
                             f'Выберите тон для предложения {step + 1}:',
                             reply_markup=keyboard)


def continue_explanation_after_friendship(bot, user):
    """Продолжает объяснительную после попытки кода дружбы"""
    start_explanation(bot, user)


def complete_explanation(bot, user):
    """Завершает написание объяснительной"""
    full_text = " ".join(user['explanation_text'])

    # Сохраняем объяснительную
    if 'obiyasnitelnay' not in user:
        user['obiyasnitelnay'] = []

    explanation_data = {
        'text': full_text,
        'emotion': user['explanation_emotion'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user['obiyasnitelnay'].append(explanation_data)
    user['obiyasnitelinee'] = user.get('obiyasnitelinee', 0) + 1

    # Очищаем временные данные
    if 'explanation_step' in user:
        del user['explanation_step']
    if 'explanation_text' in user:
        del user['explanation_text']
    if 'explanation_emotion' in user:
        del user['explanation_emotion']

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Переход: холл"))

    bot.send_message(user['id'],
                     f'Объяснительная написана и сохранена!\n\n{full_text}\n\nВсего объяснительных: {user["obiyasnitelinee"]}',
                     reply_markup=keyboard)


def show_general_menu(bot, user, all_users):
    """Показывает общее меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="👥 Кто в комнате"))
    keyboard.add(types.KeyboardButton(text="ℹ️ Инфо об игроке"))
    keyboard.add(types.KeyboardButton(text="📄 Все объяснительные"))
    keyboard.add(types.KeyboardButton(text="↩️ Назад"))

    bot.send_message(user['id'],
                     '📋 Общее меню:',
                     reply_markup=keyboard)


def show_room_users(bot, user, all_users):
    """Показывает всех пользователей в комнате"""
    if not all_users:
        bot.send_message(user['id'], 'В комнате никого нет.')
        return

    users_list = []
    for u in all_users:
        if u['id'] != user['id']:
            users_list.append(f"👤 {u['name']}")

    if users_list:
        bot.send_message(user['id'], 'В комнате находятся:\n' + '\n'.join(users_list))
    else:
        bot.send_message(user['id'], 'В комнате кроме вас никого нет.')


def show_player_info(bot, user, target_name):
    """Показывает информацию об игроке"""
    from library import users

    target_user = None
    for u in users:
        if u['name'].lower() == target_name.lower():
            target_user = u
            break

    if not target_user:
        bot.send_message(user['id'], f'Игрок с именем "{target_name}" не найден.')
        return

    info = f"""
📊 Информация об игроке:
👤 Имя: {target_user['name']}
🆔 ID: {target_user['id']}
📍 Локация: {target_user.get('location', 'Неизвестно')}

📈 Статистика:
⚡ Энергия: {target_user.get('energy', 0)}%
🍎 Еда: {target_user.get('food', 0)}%
💧 Вода: {target_user.get('water', 0)}%
🌟 Опыт: {target_user.get('experience', 0)}

🎒 Инвентарь: {', '.join(target_user.get('inventory', [])) or 'Пусто'}
🎯 Цель: {target_user.get('ochota', 1)}
📝 Объяснительных: {target_user.get('obiyasnitelinee', 0)}
    """

    # Добавляем статистику кода дружбы, если есть
    if 'friendship_stats' in target_user:
        stats = target_user['friendship_stats']
        info += f"""
🤝 Код дружбы:
   Всего попыток: {stats['total_attempts']}
   Правильных: {stats['correct_attempts']}
   Подряд правильных: {stats['consecutive_correct']}
   Подряд неправильных: {stats['consecutive_wrong']}
"""

    if 'ingas_favorite' in target_user.get('inventory', []):
        info += f"\n❤️ Любимчик Инги (с {target_user.get('became_favorite_date', 'неизвестно')})"

    bot.send_message(user['id'], info)


def show_all_explanations(bot, user):
    """Показывает все объяснительные всех игроков"""
    from library import users

    all_explanations = []

    for u in users:
        if 'obiyasnitelnay' in u and u['obiyasnitelnay']:
            count = len(u['obiyasnitelnay'])
            explanations = f"👤 {u['name']} - {count} объяснительных:\n"

            for i, exp in enumerate(u['obiyasnitelnay'], 1):
                preview = exp['text'][:50] + "..." if len(exp['text']) > 50 else exp['text']
                explanations += f"  {i}. {exp['timestamp']}: {preview}\n"

            all_explanations.append(explanations)

    if all_explanations:
        message = "📄 Все объяснительные:\n\n" + "\n".join(all_explanations)
        if len(message) > 4000:
            for i in range(0, len(message), 4000):
                bot.send_message(user['id'], message[i:i + 4000])
        else:
            bot.send_message(user['id'], message)
    else:
        bot.send_message(user['id'], 'Пока никто не написал объяснительных.')


def user_enters_location(bot, user, location, all_users):
    check_inga_status()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Проверяем предметы для использования
    if 'fake_alarm' in user.get('inventory', []):
        keyboard.add(types.KeyboardButton(text="🚨 Использовать фейк-сигнализацию"))

    if 'explanation_cancel' in user.get('inventory', []):
        keyboard.add(types.KeyboardButton(text="📝 Использовать отмену объяснительной"))

    # Проверяем, любимчик ли Инги
    if 'ingas_favorite' in user.get('inventory', []):
        show_inga_favorite_menu(bot, user)
        return

    # Проверяем цель прихода
    ochota = user.get('ochota', 1)

    if ochota == 0:
        # Пришел за карточкой или по делу
        if INGA_PRESENCE:
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Карточку взять"))
            keyboard.add(types.KeyboardButton(text="Сушки попросить"))
            keyboard.add(types.KeyboardButton(text="Ударить Ингу"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            bot.send_message(user['id'],
                             'Инга Александровна: "Ну что тебе нужно, студент?"',
                             reply_markup=keyboard)
        else:
            # Инги нет, можно действовать свободно
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Карточку взять"))
            keyboard.add(types.KeyboardButton(text="Сушки взять"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'],
                             'Инги Александровны нет на месте! Можно действовать свободно.',
                             reply_markup=keyboard)

    elif ochota == 1:
        # Просто пришел
        if INGA_PRESENCE:
            if random.randint(1, 2) == 1:
                # Отправляют писать объяснительную
                bot.send_message(user['id'],
                                 'Инга Александровна: "Опять ты тут?! Садись писать объяснительную!"')
                user['ochota'] = 2
                start_explanation_with_friendship(bot, user)
                return
            else:
                # Просто выгоняют
                keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
                keyboard.add(types.KeyboardButton(text="Переход: холл"))
                bot.send_message(user['id'],
                                 'Инга Александровна: "Уходи отсюда, не мешай работать!"',
                                 reply_markup=keyboard)
        else:
            # Инги нет, можно отдохнуть
            keyboard.add(types.KeyboardButton(text="Чайку попить"))
            keyboard.add(types.KeyboardButton(text="Сушки взять"))
            keyboard.add(types.KeyboardButton(text="Просто посидеть"))
            keyboard.add(types.KeyboardButton(text="Спросить код дружбы"))
            keyboard.add(types.KeyboardButton(text="Выйти"))
            bot.send_message(user['id'],
                             'Инги Александровны нет! Можно расслабиться.',
                             reply_markup=keyboard)

    elif ochota == 2:
        # Пришел писать объяснительную
        start_explanation_with_friendship(bot, user)
        return

    elif ochota == 3:
        # Принудительно отправлен писать объяснительную
        bot.send_message(user['id'],
                         'Инга Александровна: "Ты думал, убежишь?! Садись и пиши объяснительную!"')
        start_explanation_with_friendship(bot, user)
        return

    # Общее меню
    keyboard.add(types.KeyboardButton(text="📋 Общее меню"))
    bot.send_message(user['id'], 'Что выберете?', reply_markup=keyboard)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете 105')


# В функцию user_message добавляем:

def user_message(bot, message, user, location, all_users):
    check_inga_status()

    # Обработка использования предметов
    if message == "🚨 Использовать фейк-сигнализацию":
        if 'fake_alarm' in user.get('inventory', []):
            user['inventory'].remove('fake_alarm')
            # Активируем эффект - Инга уходит на 10 минут
            from locations.room105 import inga_goes_away
            away_minutes = inga_goes_away()
            bot.send_message(user['id'],
                             f"🚨 Сработала фейк-сигнализация! Инга Александровна вышла на {away_minutes} минут.")
            user_enters_location(bot, user, location, all_users)
        return

    elif message == "📝 Использовать отмену объяснительной":
        if 'explanation_cancel' in user.get('inventory', []):
            user['inventory'].remove('explanation_cancel')
            if user.get('ochota') in [2, 3]:
                user['ochota'] = 1
                bot.send_message(user['id'],
                                 "✅ Объяснительная отменена! Инга Александровна: 'Ладно, в этот раз прощаю.'")
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Переход: холл"))
                bot.send_message(user['id'], 'Вы можете идти.', reply_markup=keyboard)
            else:
                bot.send_message(user['id'], "У вас нет активной объяснительной для отмены.")
        return


    # Проверяем, является ли пользователь любимчиком Инги
    if 'ingas_favorite' in user.get('inventory', []):
        handle_inga_favorite_choice(bot, user, message)
        return

    # Проверяем, находится ли пользователь в процессе ввода кода дружбы
    if user.get('friendship_step') is not None and message in FRIENDSHIP_PHRASES_POOL:
        process_friendship_input(bot, user, message)
        return

    # Обработка общего меню
    if message == "📋 Общее меню":
        show_general_menu(bot, user, all_users)
        return
    elif message == "👥 Кто в комнате":
        show_room_users(bot, user, all_users)
        return
    elif message == "ℹ️ Инфо об игроке":
        bot.send_message(user['id'], 'Введите имя игрока:')
        user['awaiting_player_name'] = True
        return
    elif message == "📄 Все объяснительные":
        show_all_explanations(bot, user)
        return
    elif message == "↩️ Назад":
        # Возвращаемся к основному меню
        user_enters_location(bot, user, location, all_users)
        return

    # Обработка кода дружбы
    if message == "Спросить код дружбы":
        if user.get('ochota') in [2, 3]:
            bot.send_message(user['id'], 'Инга Александровна: "Сначала разберись с объяснительной!"')
        else:
            start_friendship_code(bot, user, during_explanation=False)
        return

    # Обработка объяснительной с кодом дружбы
    if message == "Попробовать код дружбы":
        if user.get('ochota') in [2, 3]:
            start_friendship_code(bot, user, during_explanation=True)
        return

    if message == "Продолжить объяснительную":
        continue_explanation_after_friendship(bot, user)
        return

    if message == "Начать писать объяснительную":
        start_explanation(bot, user)
        return

    # Обработка ввода имени игрока
    if user.get('awaiting_player_name'):
        del user['awaiting_player_name']
        show_player_info(bot, user, message)
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
                else:
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Какой еще чай?! Садись писать объяснительную!"')
                    user['ochota'] = 2
                    start_explanation_with_friendship(bot, user)
                    return

            elif message == "Карточку взять":
                if 'card' not in user['inventory']:
                    user['inventory'].append('card')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Чайку попить"))
                keyboard.add(types.KeyboardButton(text="Переход: холл"))
                bot.send_message(user['id'],
                                 'Инга Александровна: "На, держи свою карточку."\nКарточка добавлена в инвентарь.',
                                 reply_markup=keyboard)

            elif message == "Сушки попросить":
                if random.randint(1, 3) == 1:
                    user['food'] = min(100, user.get('food', 0) + 15)
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Возьми сушки."\nВы съели сушки. +15 сытости.')
                else:
                    bot.send_message(user['id'],
                                     'Инга Александровна: "Сушки?! Ты еще и есть хочешь?! Объяснительную пиши!"')
                    user['ochota'] = 2
                    start_explanation_with_friendship(bot, user)
                    return

            elif message == "Ударить Ингу":
                bot.send_message(user['id'],
                                 'Вы попытались ударить Ингу Александровну, но она оказалась быстрее!\n'
                                 '"В 105 на объяснительную!"')
                user['ochota'] = 2
                start_explanation_with_friendship(bot, user)
                return

        else:
            # Инги нет
            if message == "Чайку попить":
                user['energy'] = min(100, user.get('energy', 0) + 10)
                user['water'] = min(100, user.get('water', 0) + 20)
                bot.send_message(user['id'], 'Вы попили чай. +10 энергии, +20 воды.')

            elif message == "Карточку взять":
                if 'card' not in user['inventory']:
                    user['inventory'].append('card')
                bot.send_message(user['id'], 'Вы взяли карточку со стола.')

            elif message == "Сушки взять":
                user['food'] = min(100, user.get('food', 0) + 15)
                bot.send_message(user['id'], 'Вы взяли сушки. +15 сытости.')

            elif message == "Выйти":
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Переход: холл"))
                bot.send_message(user['id'], 'Вы вышли из кабинета.', reply_markup=keyboard)

    # Обработка для ochota = 1 (просто пришел)
    elif ochota == 1:
        if INGA_PRESENCE:
            # Если Инга на месте, обрабатываем только переход
            if message.startswith('Переход: '):
                if message == 'Переход: холл':
                    transfer_user(user, 'hall')
                else:
                    bot.send_message(user['id'], 'Отсюда можно выйти только в холл.')
        else:
            # Инги нет
            if message == "Чайку попить":
                user['energy'] = min(100, user.get('energy', 0) + 10)
                user['water'] = min(100, user.get('water', 0) + 20)
                bot.send_message(user['id'], 'Вы попили чай. +10 энергии, +20 воды.')

            elif message == "Сушки взять":
                user['food'] = min(100, user.get('food', 0) + 15)
                bot.send_message(user['id'], 'Вы взяли сушки. +15 сытости.')

            elif message == "Просто посидеть":
                user['energy'] = min(100, user.get('energy', 0) + 5)
                bot.send_message(user['id'], 'Вы посидели в тишине. +5 энергии.')

            elif message == "Выйти":
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Переход: холл"))
                bot.send_message(user['id'], 'Вы вышли из кабинета.', reply_markup=keyboard)

    # Обработка написания объяснительной
    elif ochota in [2, 3]:
        if message in ["Очень добрый тон", "Добрый тон", "Нейтральный тон", "Злой тон", "Очень злой тон"]:
            continue_explanation(bot, user, message)
            return

    # Обработка переходов
    elif message.startswith('Переход: '):
        if message == 'Переход: холл':
            transfer_user(user, 'hall')
        else:
            bot.send_message(user['id'], 'Отсюда можно выйти только в холл.')

    # Общая обработка
    else:
        # Если это не специальное сообщение, добавляем общее меню
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="📋 Общее меню"))
        bot.send_message(user['id'], 'Я вас не понял. Что вы хотите сделать?', reply_markup=keyboard)


def run_events(bot, location, all_users):
    """Ежедневная генерация нового кода дружбы в 00:00"""
    global CURRENT_FRIENDSHIP_CODE, CODE_LAST_UPDATED

    now = datetime.now()

    # Если сейчас около 00:00 и код еще не обновлялся сегодня
    if now.hour == 0 and now.minute < 5:
        if CODE_LAST_UPDATED != now.date():
            generate_friendship_code()

    check_inga_status()