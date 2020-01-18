
from django.db import models

class RoomData(models.Model):
    room_ip = models.CharField(max_length=50)
    room_data = models.CharField(max_length=1001)