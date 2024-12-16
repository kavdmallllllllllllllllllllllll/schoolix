

from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Chat, ChatRoom
from .serializers import ChatSerializer, TeacherSerializer, StudentSerializer, ChatRoomSerializer
from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from home.models import Teacher, Student

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_chat(request):
    if request.user.groups.filter(name__in=['manager', 'Parents', 'teacher']).exists():
        if request.method == 'GET':
            # جلب جميع الطلبة والمدرسين والمديرين
            students = Student.objects.all()
            teachers = Teacher.objects.all()
            manager_group = Group.objects.get(name='manager')
            managers = User.objects.filter(groups=manager_group)

            # تجهيز بيانات الطلبة مع ID المستخدم
            students_data = [
                {
                    "student_id": student.id,
                    "student_name": student.name,  # اسم الطالب
                    "username": student.user.username,  # اسم المستخدم
                    "user_id": student.user.id
                }
                for student in students
            ]

            # تجهيز بيانات المدرسين مع ID المستخدم
            teachers_data = [
                {
                    "teacher_id": teacher.id,
                    "teacher_name": teacher.name,  # اسم المدرس
                    "username": teacher.user.username,  # اسم المستخدم
                    "user_id": teacher.user.id
                }
                for teacher in teachers
            ]

            # تجهيز بيانات المديرين مع ID المستخدم
            managers_data = [
                {
                    "manager_id": manager.id,
                    "manager_name": manager.first_name + " " + manager.last_name,  # اسم المدير
                    "username": manager.username,  # اسم المستخدم
                    "user_id": manager.id
                }
                for manager in managers
            ]

            # تجهيز بيانات غرف الدردشة التي يشارك فيها المستخدم
            roms = ChatRoom.objects.filter(participants=request.user)
            my_roms_serializer = ChatRoomSerializer(roms, many=True)

            # البيانات النهائية للإرجاع
            response_data = {
                "Students": students_data,
                "Teachers": teachers_data,
                "Managers": managers_data,
                "My_Chat_Rooms": my_roms_serializer.data,
            }

            return Response(response_data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import ChatRoom
from .serializers import ChatRoomSerializer

User = get_user_model()
class CreateChatRoomView(generics.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        participants_ids = self.request.data.get('participants', [])

        # Convert the participants_ids to a list if it's a string (e.g., '1,2,3')
        if isinstance(participants_ids, str):
            participants_ids = participants_ids.split(',')

        # Ensure the current user is also added to the participants
        participants_ids.append(str(self.request.user.id))

        # Filter users based on the list of IDs
        participants = User.objects.filter(id__in=participants_ids)
        chat_room = serializer.save()

        # Add participants to the room
        chat_room.participants.set(participants)
        chat_room.save()


class AddParticipantsView(generics.UpdateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        room_id = self.kwargs.get('room_id')
        participants_ids = request.data.get('participants', [])

        # Ensure the room exists
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Add new participants to the room
        participants = User.objects.filter(id__in=participants_ids)
        room.participants.add(*participants)
        room.save()

        return Response({"message": "Participants added successfully"}, status=status.HTTP_200_OK)


class RoomChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room_id = self.kwargs['room_id']
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Chat.objects.none()

        if user in room.participants.all():
            return Chat.objects.filter(room=room).order_by('timestamp')
        else:
            return Chat.objects.none()

class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        room_id = self.kwargs.get('room_id')  # استخرج room_id من الـ kwargs

        # Ensure the room_id is provided
        if not room_id:
            return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the room exists
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the sender is a participant of the room
        if not room.participants.filter(id=sender.id).exists():
            return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)

        # Save the message in the room if the sender is a participant
        serializer.save(sender=sender, room=room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .models import ChatRoom, Chat
# from .serializers import ChatSerializer
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .models import ChatRoom, Chat
# from .serializers import ChatSerializer

# class SendMessageView(generics.CreateAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         sender = self.request.user
#         room_id = self.request.data.get('room_id')

#         # Ensure the room_id is provided
#         if not room_id:
#             return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure the room exists
#         try:
#             room = ChatRoom.objects.get(id=room_id)
#         except ChatRoom.DoesNotExist:
#             return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         # Ensure the sender is a participant of the room
#         if not room.participants.filter(id=sender.id).exists():
#             return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)

#         # Save the message in the room if the sender is a participant
#         serializer.save(sender=sender, room=room)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class SendMessageView(generics.CreateAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         sender = self.request.user
#         room_id = self.request.data.get('room_id')

#         # Ensure the room_id is provided
#         if not room_id:
#             return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure the room exists
#         try:
#             room = ChatRoom.objects.get(id=room_id)
#         except ChatRoom.DoesNotExist:
#             return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         # Ensure the sender is a participant of the room
#         if not room.participants.filter(id=sender.id).exists():
#             return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)

#         # Save the message in the room if the sender is a participant
#         serializer.save(sender=sender, room=room)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room_id = self.kwargs['room_id']

        # Ensure the user is a participant of the room
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Chat.objects.none()

        if user in room.participants.all():
            return Chat.objects.filter(room=room).order_by('timestamp')
        else:
            return Chat.objects.none()



class MarkAsReadView(generics.UpdateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        message_id = self.kwargs['pk']
        return Chat.objects.get(id=message_id)

    def perform_update(self, serializer):
        serializer.instance.is_read = True
        serializer.save()




# class ChatListView(generics.ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         other_user_id = self.kwargs['other_user_id']
#         return Chat.objects.filter(
#             Q(sender=user, receiver__id=other_user_id) |
#             Q(sender__id=other_user_id, receiver=user)
#         ).order_by('timestamp')



# from django.shortcuts import render
# from rest_framework import generics, permissions
# from .models import Chat, ChatRoom
# from .serializers import ChatSerializer
# from django.contrib.auth.models import User
# from django.db.models import Q
# from django.http import HttpResponse

# # View to send a message
# from django.shortcuts import render
# from rest_framework import generics, permissions
# from .models import Chat, ChatRoom
# from .serializers import ChatSerializer
# from django.contrib.auth.models import User
# from django.db.models import Q

# # View to send a message
# from rest_framework import generics, permissions
# from .models import Chat, ChatRoom
# from .serializers import ChatSerializer

# from rest_framework.response import Response
# from rest_framework import generics, status

# from django.utils import timezone
# from collections import defaultdict
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from home.models import Teacher ,Student ,Parent
# from .serializers import TeacherSerializer,StudentSerializer,ChatRoomSerializer
# from django.contrib.auth.models import User,Group

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_chat(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':

#             students= Student.objects.all()

#             teachers = Teacher.objects.all()
#             roms = ChatRoom.objects.filter(participants=request.user)  # Get rooms where the user is a participant
#             manager_group = Group.objects.get(name='manager')

#             managers = User.objects.filter(groups=manager_group)
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Serialize Teacher objects
#             Parents_serializer=StudentSerializer(students,many=True)
#             my_roms=ChatRoomSerializer(roms,many=True)

#             # Prepare the response data
#             response_data = {
#                 'Teachers': teacher_serializer.data,  # Correctly serialize Teacher data
#                 'pearans':Parents_serializer.data,
#                 'my_roms':my_roms.data,
#                 'Managers': [user.username for user in managers]  # Serialize usernames of managers
#             }

#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)











# class RoomChatListView(generics.ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         room_id = self.kwargs['room_id']
#         room = ChatRoom.objects.get(id=room_id)

#         # التحقق من أن المستخدم عضو في الغرفة
#         if user in room.participants.all():
#             return Chat.objects.filter(room=room).order_by('timestamp')
#         else:
#             return Chat.objects.none()
# class SendMessageView(generics.CreateAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         sender = self.request.user
#         room_id = self.request.data.get('room_id')

#         # Retrieve the room by ID
#         room = ChatRoom.objects.get(id=room_id)

#         # Save the message in the determined room with the sender
#         serializer.save(sender=sender, room=room)

# # class SendMessageView(generics.CreateAPIView):
# #     serializer_class = ChatSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_create(self, serializer):
# #         sender = self.request.user
# #         receiver_id = self.request.data.get('receiver')
# #         room_id = self.request.data.get('room_id')

# #         # Retrieve the receiver
# #         receiver = User.objects.get(id=receiver_id)

# #         # Retrieve the room by ID if provided, else find a room with both participants
# #         if room_id:
# #             room = ChatRoom.objects.get(id=room_id)
# #         else:
# #             room = ChatRoom.objects.filter(
# #                 participants=sender
# #             ).filter(participants=receiver).first()

# #             # If no room exists, create a new room
# #             if not room:
# #                 room = ChatRoom.objects.create(name=f"{sender.username} and {receiver.username} Room")
# #                 room.participants.add(sender, receiver)

# #         # Save the message in the determined room
# #         serializer.save(sender=sender, receiver=receiver, room=room)

# # class SendMessageView(generics.CreateAPIView):
# #     serializer_class = ChatSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_create(self, serializer):
# #         sender = self.request.user
# #         receiver = User.objects.get(id=self.request.data.get('receiver'))

# #         # البحث عن غرفة دردشة موجودة بين المستخدمين
# #         room = ChatRoom.objects.filter(
# #             participants=sender
# #         ).filter(participants=receiver).first()

# #         # إذا لم توجد غرفة، إنشاء غرفة جديدة
# #         if not room:
# #             room = ChatRoom.objects.create(name=f"{sender.username} and {receiver.username} Room")
# #             room.participants.add(sender, receiver)

# #         # حفظ الرسالة في الغرفة المحددة
# #         serializer.save(sender=sender, receiver=receiver, room=room)

# # View to list all messages between two users
# class ChatListView(generics.ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         other_user_id = self.kwargs['other_user_id']
#         return Chat.objects.filter(
#             Q(sender=user, receiver__id=other_user_id) |
#             Q(sender__id=other_user_id, receiver=user)
#         ).order_by('timestamp')

# # View to mark a message as read
# class MarkAsReadView(generics.UpdateAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         message_id = self.kwargs['pk']
#         return Chat.objects.get(id=message_id)

#     def perform_update(self, serializer):
#         serializer.instance.is_read = True
#         serializer.save()

# # def chat_page(request):
# #     return render(request, 'chat.html')