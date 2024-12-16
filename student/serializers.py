
from rest_framework import serializers
from home.models import Attendance, SchoolClass,Student,Teacher,Grade,Subject,Subject,Task,Principal,Schedule
from .models import Complaint

class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:

        model = Student
        fields = '__all__'
        extra_fields = ['user_id']  # Explicitly add these fields


from rest_framework import serializers
from home.models import Grade

class GradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'subject_name', 'school_class_name', 'grade', 'final_grade', 
            'exam_name', 'date'
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'subject_name', 'school_class_name', 'start_time', 'end_time']  # Adjust fields as necessary




from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'name', 'text', 'reviewed', 'user']
        read_only_fields = ['user', 'reviewed'] 
