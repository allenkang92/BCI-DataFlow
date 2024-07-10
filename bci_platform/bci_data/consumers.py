import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

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

        # 여기서 데이터베이스 작업이 필요하다면 아래와 같이 처리할 수 있습니다
        # await self.save_data_point(message)

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

    @database_sync_to_async
    def save_data_point(self, data):
        from .models import BCISession, BCIData
        session = BCISession.objects.get(id=self.session_id)
        BCIData.objects.create(
            session=session,
            timestamp=data['timestamp'],
            channel_1=data['channel_1'],
            channel_2=data['channel_2'],
            channel_3=data['channel_3'],
            channel_4=data['channel_4']
        )