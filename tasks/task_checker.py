if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/django-projects/tibia-stats')

import psutil
from tibia_stats.wsgi import *
from main.models import Tasks
import logging
import django


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
                exit()

    task_status = Tasks.objects.all().values('status')
    for task in task_status:
        if task['status'] != 'done':
            exec(open('/django-projects/tibia-stats/tasks/python add_exp_highscores.py').read())
            exit()
    exit()


if __name__ == "__main__":
    main()
