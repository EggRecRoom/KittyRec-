from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path("notification/v2", consumers.NotificationConsumer.as_asgi())
]