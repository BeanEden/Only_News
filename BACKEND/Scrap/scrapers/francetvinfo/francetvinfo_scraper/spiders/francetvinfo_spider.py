import scrapy
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../app/')))
from ETL.Load.Upload_Datalake import UploadDataLake


class FrancetvinfoSpider(scrapy.Spider):
    name = 'francetvinfo'

    def __init__(self, category=None, bucket_name='real-news', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = "https://www.francetvinfo.fr"
        self.articles = {}
        self.target_category = category
        self.bucket_name = bucket_name
        self.uploader = UploadDataLake()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, 'data', 'france')
        os.makedirs(self.data_dir, exist_ok=True)

    def start_requests(self):
        yield scrapy.Request(self.link, callback=self.parse_categories)

    def parse_categories(self, response):
        categories = response.css(
            'div.navigation-panel__mainpanel ul.navigation-panel__list.navigation-panel__rubrics-links li button span::text'
        ).getall()

        rename_map = {
            'Sciences & technologies': 'sciences',
            'Éco / Conso': 'economie',
            'Sport': 'sports',
        }

        for cat in categories:
            if cat in ['Jeux', 'Météo', 'Environnement']:
                continue

            if self.target_category and self.target_category.lower() != cat.lower():
                continue

            cat_slug = rename_map.get(cat, cat).replace('é', 'e')
            self.articles[cat_slug] = []
            url = f"{self.link}/{cat_slug}"

            yield response.follow(url, callback=self.parse_articles, meta={'category': cat_slug})

    def parse_articles(self, response):
        category = response.meta['category']
        article_links = response.css('section.taxonomy-contents article a::attr(href)').getall()

        for link in article_links:
            yield response.follow(link, callback=self.parse_article, meta={'category': category})

        next_page = response.css('a:contains("Page suivante")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_articles, meta={'category': category})

    def parse_article(self, response):
        category = response.meta['category']
        title = ''.join(response.xpath('//h1//text()[not(ancestor::span)][not(parent::i)]').getall()).strip()
        author = response.css('div.signature__names a::text').get(default='').strip()
        date = response.css('time::attr(datetime)').get(default='').strip()
        content = '\n'.join(response.css('div.c-body ::text').getall()).strip()

        self.articles[category].append({
            'title': title,
            'auteur': author,
            'date': date,
            'content': content,
            'url': response.url
        })

    def closed(self, reason):
        for category, articles in self.articles.items():
            filename = os.path.join(self.data_dir, f"{category.replace('/', '_')}.json")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)

            self.log(f"✅ Enregistré {len(articles)} articles dans {filename}")

            try:
                self.uploader.upload_file(
                    file_path=filename,
                    bucket_name=self.bucket_name,
                    object_name=os.path.basename(filename)
                )
                self.log(f"🚀 Upload réussi : {filename} → bucket {self.bucket_name}")
            except Exception as e:
                self.log(f"❌ Échec de l’upload : {filename} → {e}")


def get_francetvinfo_categories():
    import requests
    from parsel import Selector

    resp = requests.get("https://www.francetvinfo.fr")
    sel = Selector(text=resp.text)

    return [
        c for c in sel.css(
            'div.navigation-panel__mainpanel ul.navigation-panel__list.navigation-panel__rubrics-links li button span::text'
        ).getall()
        if c not in ['Jeux', 'Météo', 'Environnement']
    ]
