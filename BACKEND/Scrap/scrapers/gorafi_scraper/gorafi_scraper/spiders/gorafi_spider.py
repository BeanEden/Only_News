import scrapy
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../app/')))
from ETL.Load.Upload_Datalake import UploadDataLake

class GorafiSpider(scrapy.Spider):
    name = 'gorafi'

    def __init__(self, category=None, bucket_name='fake-news', *args, **kwargs):
        super(GorafiSpider, self).__init__(*args, **kwargs)
        self.articles = {}
        self.target_category = category
        self.bucket_name = bucket_name
        self.uploader = UploadDataLake()

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, 'data', 'france')
        os.makedirs(self.data_dir, exist_ok=True)

    def start_requests(self):
        yield scrapy.Request('https://www.legorafi.fr', callback=self.parse_categories)

    def parse_categories(self, response):
        category_links = response.css('#menu-menu-principal-1 li a::attr(href)').getall()

        for link in category_links:
            if '/category/' in link:
                category_slug = link.split('/category/')[-1].strip('/')

                if self.target_category and category_slug != self.target_category:
                    continue

                self.articles[category_slug] = []
                yield response.follow(link, self.parse, meta={'category': category_slug})

    def parse(self, response):
        category = response.meta['category']

        articles_links = response.css('.mvp-blog-story-wrap a::attr(href)').getall()
        for link in articles_links:
            yield response.follow(link, self.parse_article, meta={'category': category})

        next_page = response.css('.pagination a:contains("Suivante")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse, meta={'category': category})

    def parse_article(self, response):
        author = response.css('.mvp-author-info-name span a::text').get()
        date = response.css('.mvp-author-info-date span time::attr(datetime)').get()
        category = response.meta['category']
        title = response.css('h1::text').get()
        paragraphs = response.css('#mvp-content-main p::text').getall()        
        content = '\n'.join([p.strip() for p in paragraphs if p.strip()])

        self.articles[category].append({
            'title': title,
            'auteur': author,
            'date': date,
            'content': content,
            'url': response.url
        })

    def closed(self, reason):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        for category, articles_list in self.articles.items():
            safe_category = category.replace('/', '_')
            filename = os.path.join(data_dir, f'{safe_category}.json')

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles_list, f, ensure_ascii=False, indent=4)
            self.log(f'✅ Saved {len(articles_list)} articles to {filename}')

            try:
                self.uploader.upload_file(
                    file_path=filename,
                    bucket_name=self.bucket_name,
                    object_name=os.path.basename(filename)
                )
                self.log(f'🚀 Uploaded {filename} to bucket {self.bucket_name}')
            except Exception as e:
                self.log(f'❌ Failed to upload {filename} : {e}')
