def user_enters_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы во дворе')


def user_leaves_location(bot, user, location, all_users):
    bot.send_message(user['id'], 'Вы покидаете двор')


def user_message(bot, message, user, location, all_users):
    if message == 'Отдохнуть на лавочке':
        user['energy'] = min(100, user['energy'] + 5)
        bot.send_message(user['id'], f'Вы передохнули на лавочке, пару минут. '
                                     f'Теперь у вас {user['energy']} энергии.')
    else:
        bot.send_message(user['id'], 'Я вас не понял')
