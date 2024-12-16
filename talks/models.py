from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم الغرفة")
    participants = models.ManyToManyField(User, related_name="chat_rooms", verbose_name="المشاركون")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return self.name

class Chat(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages", verbose_name="الغرفة")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="مرسل")
    message = models.TextField(verbose_name="الرسالة")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="وقت الارسال")
    is_read = models.BooleanField(default=False, verbose_name="مقروء")

    def __str__(self):
        return f"{self.room.name}: {self.sender.username} - {self.timestamp}"
