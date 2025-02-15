from django.urls import re_path
from account.consumers import AccountConsumer
from message.consumers import MessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket/account/$', AccountConsumer.as_asgi()), 
    re_path(r'ws/socket/message/$', MessageConsumer.as_asgi()), 
]