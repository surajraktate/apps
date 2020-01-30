from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.room, name='room'),
    url(r'^(?P<room_name>[\w-]{,50})/$', views.room, name='chat_room'),]