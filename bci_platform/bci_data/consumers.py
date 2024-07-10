import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import BCISession, BCIData

class BCIDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session_group_name = f'bci_data_{self.session_id}'

        await self.channel_layer.group_add(
            self.session_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.session_group_name,
            {
                'type': 'bci_message',
                'message': message
            }
        )

    async def bci_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))