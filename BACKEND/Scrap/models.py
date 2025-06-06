from django.db import models
import hashlib

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


class News(models.Model):
    title = models.TextField()
    author = models.CharField(max_length=255)
    date = models.DateTimeField()
    content = models.TextField()
    url = models.CharField(max_length=500, unique=True)
    url_hash = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=100)
    is_fake = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['url']),
        ]

    def save(self, *args, **kwargs):
        self.url_hash = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title