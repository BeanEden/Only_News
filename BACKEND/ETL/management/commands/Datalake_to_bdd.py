from django.core.management.base import BaseCommand
import os
import json
from only_news.utils import parse_date
from Scrap.models import News
from ETL.Load.Upload_Datalake import UploadDataLake 
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Importe les fichiers JSON du Datalake vers la base de données'

    def handle(self, *args, **kwargs):
        self.stdout.write("📦 Début de l'import depuis MinIO")
        load_dotenv()

        datalake = UploadDataLake(
            endpoint_url='http://minio:9000',
            access_key=os.getenv("MINIO_USERNAME"),
            secret_key=os.getenv("MINIO_PASSWORD")
        )

        buckets = ['fake-news', 'real-news']
        for bucket in buckets:
            files = datalake.list_files(bucket)
            for filename in files:
                obj = datalake.s3.get_object(Bucket=bucket, Key=filename)
                data = json.load(obj['Body'])

                # Permet de gérer un seul objet ou une liste
                if isinstance(data, dict):
                    data = [data]                            

                for item in data:

                    date = parse_date(item['date'])
                    if date is None:
                        # gérer le cas (log, skip, valeur par défaut)
                        continue

                    News.objects.update_or_create(
                        url=item['url'],
                        defaults={
                            'title': item.get('title', ''),
                            'author': item.get('auteur', ''),
                            'date': date,
                            'content': item.get('content', ''),
                            'category': filename.replace('.json', ''),
                            'is_fake': bucket == 'fake-news'
                        }
                    )

        self.stdout.write(self.style.SUCCESS("✅ Import terminé"))
