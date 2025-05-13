from django.urls import path
from . import views

app_name = 'Scrap'

urlpatterns = [
    path('', views.start_scraping, name='start_scraping'),
]
