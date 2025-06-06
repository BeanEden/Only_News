import os
from django.conf import settings
from dateutil import parser
import re
from datetime import datetime

def get_available_sites():
    scrap_root = os.path.join(settings.BASE_DIR, 'SCRAP/scrapers')

    projects = {}
    for d in os.listdir(scrap_root):
        dir_path = os.path.join(scrap_root, d)
        cfg_path = os.path.join(dir_path, 'scrapy.cfg')

        if os.path.isdir(dir_path) and os.path.exists(cfg_path):
            projects[d.replace('_scraper', '')] = dir_path

    print(f'✅ Projets détectés: {projects}')
    return projects

def parse_date(date_str):
    # Premier essai : parser avec dateutil (gère ISO 8601)
    try:
        return parser.isoparse(date_str)
    except Exception:
        pass

    # Exemple de format français "02/06/2025 à 08h00"
    match = re.match(r"(\d{2})/(\d{2})/(\d{4}) à (\d{2})h(\d{2})", date_str)
    if match:
        day, month, year, hour, minute = match.groups()
        return datetime(int(year), int(month), int(day), int(hour), int(minute))

    # Si aucun format reconnu, renvoyer None ou lever une erreur
    return None
