from methods import *

while True:
    for location in locations:
        users = get_location_users(location['id'])

        try:
            modules[location['id']].run_events(bot, users)
        except Exception as e:
            print(e)