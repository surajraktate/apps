from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import RoomData
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = None
        if len(self.scope['url_route']['kwargs'])> 0:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.room_name:
            self.room_name = self.scope.get("client")[0]
        print(self.scope['url_route']['kwargs'], '__________________')

        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        try:
            room_data_obj = RoomData.objects.get(room_ip=self.room_name)
            print(room_data_obj.room_data)
        except Exception as e:
            print(e)
        else:
            self.chat_message({"message":room_data_obj.room_data})
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.store_message_into_database(message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def store_message_into_database(self, message):
        room_data_obj = None
        self.room_name = self.scope.get("client")[0]
        try:
            room_data_obj = RoomData.objects.get(room_ip=self.room_name)
        except Exception as e:
            print(e)
        else:
            room_data_obj.room_data = message
            room_data_obj.save()

        if not room_data_obj:
            try:
                room_data_obj = RoomData(room_ip=self.room_name , room_data=message)
            except Exception as e:
                print(e,"Second")
            else:
                room_data_obj.save()
                print(room_data_obj)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
