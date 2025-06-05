from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from API.views.bluesky_views import *
from API.views.scrap_views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Only News",
      default_version='v1',
      description="Documentation API Only News",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('bluesky/timeline/', BlueSkyTimelineView.as_view(), name='bluesky-timeline'),
    path('bluesky/feed-generator/', BlueSkyFeedGeneratorView.as_view(), name='bluesky-feed-generator'),
    path('bluesky/author/feed/', BlueSkyAuthorFeedView.as_view(), name='bluesky-author-feed'),

   path('scraping/categories/', get_spider_categories, name='api_get_categories'),

]
