import time

from methods import *


def common_events(bot, user):
    if random.randint(1, 5) == 1:
        user['food'] = max(0, user['energy'] - 1)
    if random.randint(1, 5) == 1:
        user['water'] = max(0, user['water'] - 1)


while True:
    for user in users:
        common_events(bot, user)

    for location in locations:
        location_users = get_location_users(location['id'])

        try:
            modules[location['id']].run_events(bot, location, location_users)
        except Exception as e:
            print(e)

    time.sleep(60)
