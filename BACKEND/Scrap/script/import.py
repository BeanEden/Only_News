import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from .import_news import import_news_from_directory

# Exemple : appel des deux répertoires
import_news_from_directory('/app/data/france', is_fake=False)
import_news_from_directory('/app/data/fake', is_fake=True)
