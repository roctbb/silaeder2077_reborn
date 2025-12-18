from telebot import types
import random
from methods import *


def make_math_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Решить пример"))
    keyboard.add(types.KeyboardButton(text="Помочь соседу по парте"))
    keyboard.add(types.KeyboardButton(text="Списывать с доски"))
    keyboard.add(types.KeyboardButton(text="Сделать вид что решаешь"))
    keyboard.add(types.KeyboardButton(text="Переход: холл 1 этажа"))

    return keyboard


def user_enters_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы в кабинете математики', reply_markup=make_math_keyboard())
    with open('assets/images/math_kab.jpg', 'rb') as photo:
        bot.send_photo(user['id'], photo)


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покинули кабинет математики')


def user_message(bot, message, user, location, all_users):
    if user.get('waiting_for_answer', False) and 'current_math_problem' in user:
        handle_math_answer(bot, user, message)
        return

    if message == 'Решить пример':
        with open('assets/images/Primer.jpg', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        if user['energy'] >= 3:
            user['energy'] = user['energy'] - 3

            examples = [
                {"question": "15 × 4 + 23 = ?", "answer": 83},
                {"question": "72 ÷ 8 × 3 = ?", "answer": 27},
                {"question": "45 - 18 + 27 = ?", "answer": 54},
                {"question": "56 ÷ 7 + 15 × 2 = ?", "answer": 38},
                {"question": "125 - 47 + 33 = ?", "answer": 111},
                {"question": "18 × 3 - 24 ÷ 4 = ?", "answer": 48},
                {"question": "64 ÷ 8 + 7 × 5 = ?", "answer": 43},
                {"question": "39 + 42 - 18 = ?", "answer": 63}
            ]

            example = random.choice(examples)
            user['current_math_problem'] = example  # Сохраняем текущий пример
            user['waiting_for_answer'] = True  # Флаг ожидания ответа

            bot.send_message(user['id'], f'Решите пример: {example["question"]}')
            bot.send_message(user['id'], f'Вы потратили 3% энергии. Теперь у вас {user["energy"]}% энергии.')
        else:
            bot.send_message(user['id'],
                             f'У вас не хватает энергии! Сейчас у вас {user["energy"]}% энергии. Нужно 3% энергии!')

    elif message == 'Помочь соседу по парте':
        with open('assets/images/help.jpg', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        if user['experience'] >= 2:
            x = random.randint(1, 2)
            if x == 1:
                user['experience'] = user['experience'] + 2
                bot.send_message(user['id'],
                                 f'Вы хорошо объяснили тему! Получили 4 опыта! Теперь у вас {user["experience"]} опыта!')
            elif x == 2:
                user['energy'] = max(0, user['energy'] - 5)
                bot.send_message(user['id'],
                                 f'Сосед не понял объяснение, пришлось потратить больше времени. Потеряли 5% энергии и 2 опыта. Теперь у вас {user["energy"]}% энергии и {user["experience"]} опыта.')
        else:
            bot.send_message(user['id'],
                             f'У вас недостаточно опыта чтобы помогать другим! Нужно 2 опыта, а у вас {user["experience"]}.')

    elif message == 'Списывать с доски':
        with open('assets/images/doska.jpg', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        x = random.randint(1, 4)
        if x == 1:
            bot.send_message(user['id'], 'Вас поймали на списывании! Учитель отправил писать объяснительную!')
            user['energy'] = max(0, user['energy'] - 5)
            transfer_user(user, 'room105')
        elif x == 2:
            user['experience'] = user['experience'] + 1
            bot.send_message(user['id'],
                             f'Вы успешно списали и поняли тему! Получили 1 опыт! Теперь у вас {user["experience"]} опыта!')
        else:
            bot.send_message(user['id'], 'Вы успешно списали решение!')

    elif message == 'Сделать вид что решаешь':
        with open('assets/images/tipo_reshaet.jpg', 'rb') as photo:
            bot.send_photo(user['id'], photo)
        x = random.randint(1, 3)
        if x == 1:
            bot.send_message(user['id'], 'Учитель заметил, что вы не решаете, и вызвал к доске!')
        else:
            user['energy'] = min(100, user['energy'] + 2)
            bot.send_message(user['id'],
                             f'Вам удалось отдохнуть! Восстановили 2% энергии. Теперь у вас {user["energy"]}% энергии.')

    elif message == 'Перейти во двор':
        bot.send_message(user['id'], 'Вы вышли во двор')
    else:
        bot.send_message(user['id'], 'Я вас не понял')


# Функция для обработки ответов на математические примеры
def handle_math_answer(bot, user, user_answer):
    if 'current_math_problem' in user and user.get('waiting_for_answer', False):
        try:
            answer = int(user_answer)
            correct_answer = user['current_math_problem']['answer']

            if answer == correct_answer:
                user['experience'] = user['experience'] + 1
                user['energy'] = min(100, user['energy'] + 1)
                bot.send_message(user['id'],
                                 f'✅ Правильно! Получили 1 опыт и 1% энергии! Теперь у вас {user["experience"]} опыта и {user["energy"]}% энергии!')
            else:
                bot.send_message(user['id'], f'❌ Неправильно! Правильный ответ: {correct_answer}')

            user.pop('current_math_problem', None)
            user['waiting_for_answer'] = False

        except ValueError:
            bot.send_message(user['id'], 'Пожалуйста, введите число!')
