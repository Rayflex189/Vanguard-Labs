from django.urls import path
from .views import (
    conversation_list, conversation_detail, send_message,
    mark_conversation_read, unread_count, create_conversation
)

app_name = 'messaging'

urlpatterns = [
    path('', conversation_list, name='list'),
    path('new/', create_conversation, name='create'),
    path('<int:pk>/', conversation_detail, name='detail'),
    path('<int:pk>/send/', send_message, name='send'),
    path('<int:pk>/read/', mark_conversation_read, name='mark_read'),
    path('unread-count/', unread_count, name='unread_count'),
]
