import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # id of the current user
        my_id= self.scope['user'].id
        # my_id= self.scope['user']
        print(my_id)

        # id of user with whom we are chatting
        user_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(user_id):
            self.room_name = f'{my_id}-{user_id}'
            
        else:
            self.room_name = f'{user_id}-{my_id}'

        self.room_group_name = 'chat_%s'% self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        # getting it from the frontend
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self,event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # using decorator more working with the models and the databases
    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        Chat.objects.create(sender=username, message=message, thread_name=thread_name)