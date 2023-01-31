if __name__ == '__main__':
    import sys

    sys.path.insert(0, '/django-projects/tibia-stats')
import psutil


def main():
    check_running_tasks()


def check_running_tasks():
    running_tasks = []
    for i in psutil.pids():
        if psutil.Process(i).name() == 'python':
            running_tasks.append(psutil.Process(i).cmdline())

    '''running_tasks = [['/django-projects/tibia-stats/venv-tibia-stats/bin/python',
                      '/django-projects/tibia-stats/tasks/add_exp_highscores.py'],
                     ['python', 'a.py']]'''
    for current_task in running_tasks:
        name = current_task[-1].split("/")
        if name[-1] == "add_exp_highscores.py":
            exit()
        else:
            pass
            # wywolanie pliku


if __name__ == "__main__":
    main()
