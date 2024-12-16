


from django.urls import path
from .views import (
    RoomChatListView, SendMessageView, home_chat, MarkAsReadView, ChatListView,
    CreateChatRoomView, AddParticipantsView
)

urlpatterns = [
    path('', home_chat, name='home_chat'),
    path('rooms/<int:room_id>/', RoomChatListView.as_view(), name='room_chat_list'),
    path('rooms/<int:room_id>/send_message/', SendMessageView.as_view(), name='send_message'),  # تعديل هنا
    path('chat/<int:room_id>/', ChatListView.as_view(), name='chat_list'),
    path('mark_as_read/<int:pk>/', MarkAsReadView.as_view(), name='mark_as_read'),
    path('create_room/', CreateChatRoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/add_participants/', AddParticipantsView.as_view(), name='add_participants'),
]