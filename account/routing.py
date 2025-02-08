from django.urls import re_path
from account.consumers import MyConsumer  # Import your WebSocket consumer

websocket_urlpatterns = [
    re_path(r'ws/somepath/$', MyConsumer.as_asgi()),  # Make sure this matches your WebSocket request
]