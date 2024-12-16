
# Serializers
from rest_framework import serializers
from .models import ChatRoom, Chat
from home.models import Teacher, Student, SchoolClass
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Chat

from rest_framework import serializers
from .models import Chat
from rest_framework import serializers
from .models import Chat



# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = ['room', 'sender', 'message', 'timestamp']  # Ensure 'room', 'sender', and 'message' are included
#         read_only_fields = ['sender', 'room', 'timestamp']

#     def create(self, validated_data):
#         # يتم تعيين البيانات بشكل صحيح داخل الـ view
#         return Chat.objects.create(**validated_data)









class ChatSerializer(serializers.ModelSerializer):
    sender_display = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['room', 'sender', 'message', 'timestamp', 'sender_display']
        read_only_fields = ['sender', 'room', 'timestamp']

    def get_sender_display(self, obj):
        user = self.context['request'].user
        if obj.sender == user:
            return 'me'
        return obj.sender.username
    def create(self, validated_data):
        # يتم تعيين البيانات بشكل صحيح داخل الـ view
        return Chat.objects.create(**validated_data)





# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = ['room', 'sender', 'message', 'timestamp']  # Ensure 'room', 'sender', and 'message' are included
#         read_only_fields = ['sender', 'room', 'timestamp']

#     def create(self, validated_data):
#         # يتم تعيين البيانات بشكل صحيح داخل الـ view
#         return Chat.objects.create(**validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Teacher
        fields = ['user', 'name', 'image', 'is_class_representative', 'phon', 'notes']

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    SchoolClass_data = serializers.SlugRelatedField(
        queryset=SchoolClass.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Student
        fields = ['user', 'name', 'image', 'ago', 'adres', 'father', 'file_namber', 'SchoolClass_data', 'info']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants', 'created_at']





# from rest_framework import serializers
# from .models import Chat
# from home.models import Teacher,Student,SchoolClass,Subject
# from django.contrib.auth.models import User

# from rest_framework import serializers
# from .models import Chat

# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = ['id', 'room', 'sender', 'message', 'timestamp', 'is_read']
#         read_only_fields = ['sender', 'timestamp', 'is_read']


# class TeacherSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username',  # Change this to 'username'
#     )

#     class Meta:
#         model = Teacher
#         fields = ['user', 'name', 'image', 'is_class_representative', 'phon', 'notes']

# # Subject


# class StudentSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username',  # Change this to 'username'
#     )
#     SchoolClass_data = serializers.SlugRelatedField(
#         queryset=SchoolClass.objects.all(),
#         slug_field='name',  # Change this to 'username'
#     )
#     class Meta:
#         model = Student
#         fields = ['user', 'name', 'image', 'ago', 'adres', 'father', 'file_namber', 'SchoolClass_data','info']
# from rest_framework import serializers
# from .models import ChatRoom

# class ChatRoomSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ChatRoom
#         fields = ['id', 'name', 'participants', 'created_at']  # Adjust fields as necessary

# # class Student(models.Model):
# #     class Meta:
# #         verbose_name_plural = " الطالب"
# #     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
# #     name = models.CharField(max_length=150)
# #     image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
# #     ago = models.CharField(max_length=150, verbose_name="السن")
# #     adres = models.TextField(verbose_name="عنوان السكن")
# #     file_namber = models.CharField(max_length=150, verbose_name="رقم الملف")
# #     father = models.CharField(max_length=150, verbose_name="اسم ولي الأمر")
# #     father_nammber = models.CharField(max_length=150, verbose_name="رقم ولي الأمر")
# #     SchoolClass_data = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
# #     info = models.TextField(verbose_name="ملحوظات عامة", null=True, blank=True)

# #     def __str__(self):
# #         return self.name
# #     def save(self, *args, **kwargs):
# #         super().save(*args, **kwargs)  # حفظ بيانات المدرس أولاً
# #         teacher_group, created = Group.objects.get_or_create(name='Parents')
# #         if self.user and not self.user.groups.filter(name='Parents').exists():
# #             self.user.groups.add(teacher_group)
# # # نموذج الدرجات








# # # نموذج المدرس
# # class Teacher(models.Model):
# #     class Meta:
# #         verbose_name_plural = " المدرس"
# #     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
# #     name = models.CharField(max_length=150)
# #     image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
# #     is_class_representative = models.BooleanField(default=False)
# #     classes = models.ManyToManyField('SchoolClass', related_name="teachers", verbose_name="الفصول")
# #     subjects = models.ManyToManyField('Subject', related_name="teachers", verbose_name="المواد")
# #     phon= models.CharField(max_length=150, verbose_name="رقم الهاتف ", null=True, blank=True)
# #     notes=models.TextField( null=True, blank=True)
# #     def __str__(self):
# #         return self.name
# #     def save(self, *args, **kwargs):
# #         super().save(*args, **kwargs)  # حفظ بيانات المدرس أولاً
# #         teacher_group, created = Group.objects.get_or_create(name='teacher')
# #         if self.user and not self.user.groups.filter(name='teacher').exists():
# #             self.user.groups.add(teacher_group)