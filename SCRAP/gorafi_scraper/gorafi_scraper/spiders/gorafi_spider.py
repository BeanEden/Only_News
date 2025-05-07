import scrapy
import json

class GorafiSpider(scrapy.Spider):
    name = 'gorafi_spider'

    def __init__(self, *args, **kwargs):
        super(GorafiSpider, self).__init__(*args, **kwargs)
        self.articles = {}

    def start_requests(self):
        # On commence par la home pour aller chercher toutes les catégories
        yield scrapy.Request('https://www.legorafi.fr', callback=self.parse_categories)

    def parse_categories(self, response):
        # Sélectionner les liens du menu principal
        category_links = response.css('#menu-menu-principal-1 li a::attr(href)').getall()
        for link in category_links:
            if '/category/' in link:
                category_slug = link.split('/category/')[-1].strip('/')

                # Init la catégorie dans le dict
                if category_slug not in self.articles:
                    self.articles[category_slug] = []

                yield response.follow(link, self.parse, meta={'category': category_slug})

    def parse(self, response):
        category = response.meta['category']

        # Pour chaque article sur la page
        articles_links = response.css('.mvp-blog-story-wrap a::attr(href)').getall()
        for link in articles_links:
            yield response.follow(link, self.parse_article, meta={'category': category})

        # Pagination : page suivante
        next_page = response.css('.pagination a:contains("Suivante")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse, meta={'category': category})

    def parse_article(self, response):
        category = response.meta['category']
        title = response.css('h1::text').get()
        paragraphs = response.css('#mvp-content-main p::text').getall()
        content = '\n'.join([p.strip() for p in paragraphs if p.strip()])

        self.articles[category].append({
            'title': title,
            'content': content,
            'url': response.url
        })

    def closed(self, reason):
        filename = f'articles_all.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=4)
        self.log(f'Saved file {filename}')
