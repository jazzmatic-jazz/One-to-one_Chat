from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns =[
    path('ws/<int:id>/', MyConsumer.as_asgi()),
]