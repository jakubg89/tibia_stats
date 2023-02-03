if __name__ == '__main__':
    import sys

    sys.path.insert(0, '/django-projects/tibia-stats')
    from scripts.database.add_data import (scrap_charms,
                                           scrap_experience,
                                           prepare_data_and_db,
                                           insert_name_change,
                                           insert_world_changes,
                                           insert_highscores,
                                           get_daily_records)
from tibia_stats.wsgi import *
from main.models import Tasks
from datetime import datetime
import datetime
import logging
import glob
import os
import django


os.environ["DJANGO_SETTINGS_MODULE"] = 'tibia_stats.settings'
django.setup()

# Task status:
# queued
# done


def main():
    # now = datetime.datetime.now()
    # date = now - timedelta(days=1, hours=2)
    # delete_files()
    date = datetime.datetime.now()
    if start_time():
        logging.info(f'{datetime.datetime.now()} TASK START')
        delete_tasks()
        logging.info(f'{datetime.datetime.now()} Tasks deleted.')
        # delete_files()
        logging.info(f'{datetime.datetime.now()} Files deleted.')
        create_tasks(date)
        logging.info(f'{datetime.datetime.now()} Tasks created.')
        perform_script()
    else:
        perform_script()


def perform_script():
    logging.info(f'{datetime.datetime.now()} Perform script started.')

    list_and_date = get_tasks_to_list()
    if list_and_date:
        to_do = list_and_date['to_do']
        date = list_and_date['date']
        for i in to_do:
            logging.info(f'Performing {i} - {datetime.datetime.now()}')
            eval(i + '(date)')
    else:
        logging.info(f'{datetime.datetime.now()} All tasks are done. EXIT')
        exit()


def delete_tasks():
    clear_data_query = Tasks.objects.all()
    clear_data_query._raw_delete(clear_data_query.db)


def delete_files():
    for file in glob.glob("G:\\Python nauka\\django\\strony\\tibia_stats\\temp\\"):
        os.remove(file)


def start_time():
    start = datetime.time(3, 45, 0)
    end = datetime.time(4, 15, 0)
    current = datetime.datetime.now().time()
    return start <= current <= end


def create_tasks(date):
    tasks = {}
    status = "queued"
    tasks_list = [
        "scrap_experience",
        "scrap_charms",
        "prepare_data_and_db",
        "insert_name_change",
        "insert_world_changes",
        "insert_highscores",
        "get_daily_records",
        # "move_only_active_players",
        # "delete_old_highscores_date"
    ]

    for idx, i in enumerate(tasks_list):
        tasks.update({idx: {
            "task_name": i,
            "status": status,
            "date": date
        }})
    tasks_for_insert = []
    for task in tasks:
        task_obj = Tasks(
            task_name=tasks[task]["task_name"],
            status=tasks[task]["status"],
            date=tasks[task]["date"]
        )
        tasks_for_insert.append(task_obj)
    Tasks.objects.bulk_create(tasks_for_insert)
    logging.info('Tasks created.')


def get_tasks_to_list():
    get_tasks = Tasks.objects.all().values('task_name', 'status', 'date').order_by('task')

    if get_tasks:
        to_do = []
        for i in get_tasks:
            if (i['status'] != 'done') and (i['task_name'] != "checked_characters"):
                to_do.append(i["task_name"])
        list_and_date = {'date': get_tasks[0]['date'],
                         'to_do': to_do}
        return list_and_date
    else:
        logging.info(f'{datetime.datetime.now()} All tasks are done. EXIT')
        exit()


if __name__ == "__main__":
    main()

