import os
import django

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/django-projects/tibia-stats')
    from scripts.database.add_data import (filter_highscores_data,
                                           move_only_active_players,
                                           delete_old_highscores_date)

os.environ["DJANGO_SETTINGS_MODULE"] = 'tibia_stats.settings'
django.setup()

filter_highscores_data()
move_only_active_players()
delete_old_highscores_date()
