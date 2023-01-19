import os
import django

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/django-projects/tibia-stats')
    from scripts.database.data import filter_highscores_data


os.environ["DJANGO_SETTINGS_MODULE"] = 'tibia_stats.settings'
django.setup()

filter_highscores_data()

