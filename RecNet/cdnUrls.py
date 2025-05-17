from django.urls import include, path
from core import cdnviews

urlpatterns = [
    path('img/<path:path>', cdnviews.img),
    path('video/<path:path>', cdnviews.video),
    path('audio/<path:path>', cdnviews.audio),
]