import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode, exceptions as jwt_exceptions
from django.conf import settings
from account.models import User
from urllib.parse import parse_qs


class SocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_jwt()
        if not self.user:
            await self.close()
        else:
            self.user_group_name = f"user_{self.user.id}"

            await self.channel_layer.group_add(self.user_group_name, self.channel_name)
            await self.channel_layer.group_add("broadcast", self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

        await self.channel_layer.group_discard("broadcast", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get("type")

        if msg_type == "chat":
            await self.handle_chat(data)
        elif msg_type == "notification":
            await self.handle_notification(data)

    async def handle_chat(self, data):
        sender_id = self.user.id
        # sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        message = data.get("message")

        # Save Message
        await self.save_message(sender_id, receiver_id, message)

        # Send message to sender and receiver groups
        for uid in [sender_id, receiver_id]:
            await self.channel_layer.group_send(
                f"user_{uid}",
                {
                    "type": "chat_message",
                    "message": message,
                    "from": sender_id,
                    "to": receiver_id,
                    # "from": receiver_id,
                    # "to": sender_id,
                }
            )

    async def handle_notification(self, data):
        message = data.get("message")

        await self.channel_layer.group_send(
            "broadcast",
            {
                "type": "broadcast_notification",
                "message": message,
                "from": self.user.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "from": event["from"],
            "to": event["to"]
        }))

    async def broadcast_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"],
            "from": event["from"]
        }))

    @database_sync_to_async
    def get_user_from_jwt(self):
        try:
            query_string = self.scope["query_string"].decode()
            params = parse_qs(query_string)
            token = params.get("token", [None])[0]

            if not token:
                return None

            payload = jwt_decode(
                token,
                settings.SECRET_KEY,  # or settings.SIMPLE_JWT['SIGNING_KEY']
                algorithms=["HS256"],  # Make sure this matches token algorithm
                options={"verify_aud": False}  # disable audience check if not used
            )

            user_id = payload.get("user_id") or payload.get("userId")
            if not user_id:
                return None

            return User.objects.get(id=user_id)

        except jwt_exceptions.ExpiredSignatureError:
            print("JWT Decode Error: Token has expired")
            return None
        except jwt_exceptions.InvalidSignatureError:
            print("JWT Decode Error: Signature verification failed")
            return None
        except Exception as e:
            print("JWT Decode Error:", e)
            return None
        
    
    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message_text):
        from message.models import Message  # adjust import path if needed

        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_text=message_text
        )