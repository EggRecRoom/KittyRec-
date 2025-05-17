from django.urls import include, path
from core import emailviews

urlpatterns = [
    path('ls/click', emailviews.emailw),
]