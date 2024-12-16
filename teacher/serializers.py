from rest_framework import serializers
from home.models import Teacher,Attendance,Student,Task,SchoolClass,Subject
from. models import Academic_tasks

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk','title', 'description', 'assigned_by', 'assigned_to', 'due_date', 'is_completed']


class Task_updet_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_completed']

class SchoolClass_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['pk','name']

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk','name']

class Attendance_Serializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        label="تم التكليف إلى"
    )

    class Meta:
        model = Attendance
        fields = ['pk', 'school_class', 'date', 'student', 'teacher', 'is_present']


from rest_framework import serializers
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    classes = SchoolClass_Serializer(many=True)
    subjects = SubjectSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['name', 'image', 'is_class_representative', 'classes', 'subjects', 'phon', 'notes']

class AcademicTasksSerializer(serializers.ModelSerializer):
    schoolclass = serializers.SlugRelatedField(
        queryset=SchoolClass.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = Academic_tasks
        fields = ['pk','name', 'task', 'schoolclass','image','date']



from rest_framework import serializers
from .models import leve_student, SchoolClass, Student

class leve_studentsSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    schoolclass_name = serializers.SerializerMethodField()

    def get_schoolclass_name(self, obj):
        # الحصول على الفصل من الطالب إذا كان موجودًا
        return obj.student.SchoolClass_data.name if obj.student and obj.student.SchoolClass_data else None

    class Meta:
        model = leve_student
        fields = [
            'pk', 'schoolclass_name', 'date', 'student', 'student_name', 'teacher',
            'teacher_name', 'is_present', 'permission_type', 'reason',
            'permission_start_time', 'permission_end_time'
        ]


    # name=models.CharField(max_length=180)
    # name=models.TextField()
    # schoolclass = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
# class Attendance_Serializer(serializers.ModelSerializer):
#     student = serializers.SlugRelatedField(
#         queryset=Student.objects.all(),
#         slug_field='name',  # This correctly references the related User's username
#         label="تم التكليف إلى"
#     )


    # class Meta:
    #     model = Attendance
    #     fields = ['pk','school_class', 'date', 'student', 'teacher', 'is_present']



# class Attendance_Serializer(serializers.ModelSerializer):
#     class_id = serializers.IntegerField(write_only=True, required=True)

#     class Meta:
#         model = Attendance
#         fields = ['pk', 'school_class', 'date', 'student', 'is_present', 'class_id']

#     def validate(self, data):
#         # Filter students by the selected class
#         class_id = data.get('class_id')
#         students = Student.objects.filter(school_class_id=class_id)

#         # Ensure the selected student belongs to the selected class
#         if data['student'] not in students:
#             raise serializers.ValidationError("The selected student does not belong to the chosen class.")

#         return data
# class Attendance(models.Model):
#     class Meta:
#         verbose_name_plural = " الغياب"
#     school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
#     date = models.DateField(default=timezone.now)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     is_present = models.BooleanField(default=True)


#     def __str__(self):
#         return f"{self.student.name} - {self.school_class.name} - {self.date}"
