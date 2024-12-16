from django.contrib.auth.models import User
from rest_framework import serializers
from.models import Principal,Teacher,Task


class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = '__all__'



# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['pk','title', 'description', 'assigned_by', 'assigned_to', 'due_date', 'is_completed']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        queryset=Teacher.objects.all(),
        slug_field='name',  # This correctly references the related User's username
        label="تم التكليف إلى"
    )
    assigned_by= serializers.SlugRelatedField( 
        queryset=Principal.objects.all(),slug_field='name',)



    class Meta:
        model = Task
        fields = ['pk', 'title', 'description', 'assigned_by', 'assigned_to', 'due_date', 'is_completed']
        extra_kwargs = {
            'title': {'label': "عنوان المهمة"},
            'description': {'label': "وصف المهمة"},
            'due_date': {'label': "تاريخ الاستحقاق"},
            'is_completed': {'label': "تمت المهمة"}
        }










from rest_framework import serializers
from .models import Attendance, SchoolClass, Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'school_class', 'student', 'date', 'teacher', 'is_present']

    def validate(self, data):
        # التحقق من أن الطالب الذي يتم تسجيل حضوره هو جزء من الفصل المحدد
        if not data['school_class'].student_set.filter(id=data['student'].id).exists():
            raise serializers.ValidationError("الطالب ليس جزءًا من هذا الفصل.")
        return data













class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']  # Include any other fields as needed

class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = ['id', 'name']  # Include any other fields as needed




# class bookingseializer(serializers.ModelSerializer):
#     class Meta:
#         model = booking
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [ 'username', 'email', 'password']

