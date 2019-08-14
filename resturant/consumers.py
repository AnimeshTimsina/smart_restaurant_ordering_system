from .models import Orders
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class checkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'order_track'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
        self.group_name,
        self.channel_name
        )

    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        table = text_data_json['table']
        food = text_data_json['food']
        quantity = text_data_json['quantity']
        dateOfCreation = text_data_json['dateOfCreation']
        costList = text_data_json['costList']
        totalCost = text_data_json['totalCost']
        order_status = text_data_json['order_status']
        id = text_data_json['id']

        
        await self.channel.layer.group_send(
            self.group_name,
            {
            'type':'broadcast',
            'table':table,
            'food':food,
            'quantity':quantity,
            'dateOfCreation':dateOfCreation,
            'costList':costList,
            'totalCost':totalCost,
            'order_status':order_status,
            'id':id,
            
            }
        )

    async def broadcast(self,event):
        table = event['table']
        food = event['food']
        quantity = event['quantity']
        dateOfCreation = event['dateOfCreation']
        costList = event['costList']
        totalCost = event['totalCost']
        order_status = event['order_status']
        id = event['id']
        await self.send(text_data=json.dumps(
            {
                'table':table,
                'food':food,
                'quantity':quantity,
                'dateOfCreation':dateOfCreation,
                'costList':costList,
                'totalCost':totalCost,
                'order_status':order_status,
                'id':id,
             


                }))
