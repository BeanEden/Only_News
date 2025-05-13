from django.contrib import admin
from .models import ScrapingLog

@admin.register(ScrapingLog)
class ScrapingLogAdmin(admin.ModelAdmin):
    list_display = ('spider_name', 'category', 'status', 'started_at')
    list_filter = ('spider_name', 'status', 'started_at')