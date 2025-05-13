import os
from django.conf import settings

def get_available_sites():
    scrap_root = os.path.join(settings.BASE_DIR, 'app/SCRAP/scrapers')

    projects = {}
    for d in os.listdir(scrap_root):
        dir_path = os.path.join(scrap_root, d)
        cfg_path = os.path.join(dir_path, 'scrapy.cfg')

        if os.path.isdir(dir_path) and os.path.exists(cfg_path):
            projects[d.replace('_scraper', '')] = dir_path

    print(f'✅ Projets détectés: {projects}')
    return projects
