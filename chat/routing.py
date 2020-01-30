from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/', consumers.ChatConsumer),
    path('ws/<room_name>/', consumers.ChatConsumer),
]