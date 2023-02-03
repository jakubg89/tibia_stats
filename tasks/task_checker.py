if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/django-projects/tibia-stats')

import psutil
from tibia_stats.wsgi import *
from main.models import Tasks
import logging
import django
import datetime
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


logging.basicConfig(
    level=logging.INFO,
    filename="/django-projects/tibia-stats/logs/task_checker.log",
    filemode="a",
)

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get("DSN"),
    integrations=[
        sentry_logging,
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


def main():
    check_running_tasks()


def check_running_tasks():
    running_tasks = []
    for i in psutil.pids():
        if psutil.Process(i).name() == 'python':
            running_tasks.append(psutil.Process(i).cmdline())

    if running_tasks:
        for current_task in running_tasks:
            name = current_task[-1].split("/")
            if name[-1] == "add_exp_highscores.py":
                logging.info(f'ADD HIGHSCORES - {datetime.datetime.now()} - '
                             f'add_exp_highscores.py running')
                exit()

    task_status = Tasks.objects.all().values('status')
    for task in task_status:
        if task['status'] != 'done':
            logging.info(f'ADD HIGHSCORES - {datetime.datetime.now()} - Executing file.')
            exec(open('/django-projects/tibia-stats/tasks/python add_exp_highscores.py').read())
            exit()

    logging.info(f'ADD HIGHSCORES - {datetime.datetime.now()} - All tasks are done.')
    exit()


if __name__ == "__main__":
    main()
