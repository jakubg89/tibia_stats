import os
import django

if __name__ == "__main__":

    import sys
    sys.path.insert(0, '/django-projects/tibia-stats')
    from scripts.database.data import add_world_online_history

os.environ["DJANGO_SETTINGS_MODULE"] = "tibia_stats.settings"
django.setup()

add_world_online_history()
