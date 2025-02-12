import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user.models import ChatHistory, ChatRoom, CustomUser
from django.db.models import Q
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    # @database_sync_to_async
    # def create_chat(self,  buyer_id,product_id, seller_id):


    #     self.product_id=product_id
    #     self.buyer_id=buyer_id
    #     self.room_detail, created=ChatRoom.objects.get_or_create( buyer_id=buyer_id, product_id=product_id,seller_id= seller_id)
        
    #   #  ChatHistory.objects.create(room=room_detail, sender=sender, message=message, receiver=receiver)
    #     return self.room_detail
    

    @database_sync_to_async
    def save_chat(self,sender, message, receiver, product,buyer,seller):
       

        room_obj=ChatRoom.objects.get(seller_id=seller, buyer_id=buyer,product_id=product)

        sender_obj=CustomUser.objects.get(id=sender)
        receiver_obj=CustomUser.objects.get(id=receiver)
        #print(room_obj)

        chat=ChatHistory.objects.create(room=room_obj,sender=sender_obj, message=message, receiver=receiver_obj)
        return chat

    # @sync_to_async
    # def get_chat(self):
    #     c1 = Q(room__product_id=self.product_id)
    #     c2 = Q(room__buyer_id=self.buyer_id)
    #     chats=ChatHistory.objects.filter(c1 & c2) 
    #     for chat in chats:
    #         print(chat.message)
    

   
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        product = text_data_json['product']
        buyer = text_data_json['buyer']
        seller = text_data_json['seller']
        sender_name = text_data_json['sender_name']



      

        



        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'sender_name': sender_name,


            }
        )
        await self.save_chat( sender, message, receiver, product,buyer,seller)
        # await self.get_chat()
        
        



    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']
        sender_name=event['sender_name']
        
        
        
           


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
           
            'message': message,
            'sender_name': sender_name,
        }))