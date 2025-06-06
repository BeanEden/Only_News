import sys
import subprocess
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import ScrapingLog
from .forms import ScrapingForm
from only_news.utils import get_available_sites

def start_scraping(request):
    sites = get_available_sites()
    choices = [(site, site.capitalize()) for site in sites.keys()]

    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        form.fields['spider'].choices = choices

        if form.is_valid():
            spider = form.cleaned_data['spider']
            category = form.cleaned_data['category']

            if spider not in sites:
                messages.error(request, f"Spider '{spider}' inconnu.")
                return redirect('Scrap:start_scraping')

            project_dir = sites[spider]

            log = ScrapingLog.objects.create(
                spider_name=spider,
                category=category or 'All',
                status='Started',
                started_at=now()
            )

            cmd = [sys.executable, '-m', 'scrapy', 'crawl', spider]
            if category:
                cmd += ['-a', f'category={category}']

            env = os.environ.copy()
            backend_dir = os.path.abspath(os.path.join(project_dir, '../../../app'))
            env["PYTHONPATH"] = f"{backend_dir}:{env.get('PYTHONPATH', '')}"

            try:
                with open('scraping_output.log', 'w') as log_file:
                    subprocess.Popen(
                        cmd,
                        cwd=project_dir,
                        stdout=log_file,
                        stderr=log_file,
                        env=env
                    )
                messages.success(request, f"Scraping '{spider}' pour la catégorie '{category}' lancé en arrière-plan ✅")
            except Exception as e:
                log.status = 'Failed'
                log.error_message = str(e)
                log.ended_at = now()
                log.save()
                messages.error(request, f"Erreur lors du lancement du scraping ❌")

            return redirect('Scrap:start_scraping')

    else:
        form = ScrapingForm()
        form.fields['spider'].choices = choices

    logs = ScrapingLog.objects.order_by('-started_at')[:20]

    return render(request, 'start_scraping.html', {'form': form, 'logs': logs})
