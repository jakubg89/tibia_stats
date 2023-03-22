import os
import django

if __name__ == "__main__":
    import sys

    sys.path.insert(0, "/django-projects/tibia-stats")
    from scripts.database.add_data import get_creature_kill_stats

os.environ["DJANGO_SETTINGS_MODULE"] = "tibia_stats.settings"
django.setup()

get_creature_kill_stats()
