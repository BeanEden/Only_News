import os
import json
from django.utils.dateparse import parse_datetime
from Scrap.models import News

def import_news_from_directory(base_dir, is_fake):
    for filename in os.listdir(base_dir):
        if not filename.endswith(".json"):
            continue

        category = filename.replace('.json', '')

        with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)

        for article in data:
            News.objects.update_or_create(
                url=article['url'],
                defaults={
                    'title': article['title'],
                    'author': article['auteur'],
                    'date': parse_datetime(article['date']),
                    'content': article['content'],
                    'category': category,
                    'is_fake': is_fake
                }
            )
