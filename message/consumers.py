from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("----Connected-------")
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Websocket Connected!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected", close_code)

    async def receive(self, text_data):
        print("===> Received", text_data)
        await self.send(text_data=json.dumps({"message": "Received", "data": text_data}))
