from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from core import wwwviews

urlpatterns = [
    path("", wwwviews.index),
    path("login", wwwviews.login),
    path("api/auth/login", wwwviews.loginApi),
    path("api/auth/session", wwwviews.sessionApi)
]
