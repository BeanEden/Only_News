from django.db import models

class ScrapingLog(models.Model):
    spider_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    output_file = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.spider_name} - {self.category or 'all'} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
