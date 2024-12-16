
from rest_framework import serializers
from home.models import Attendance, SchoolClass,Student,Teacher,Grade,Subject,Subject,Task,Principal,Schedule
from.models import info_to_Parent,TeacherAttendance,info_to_Parent_by_class,event_to_all


class AttendanceSerializer(serializers.ModelSerializer):
    student= serializers.SlugRelatedField( 
        queryset=Student.objects.all(),slug_field='name',)
    teacher= serializers.SlugRelatedField( 
        queryset=Teacher.objects.all(),slug_field='name',)
    school_class= serializers.SlugRelatedField( 
        queryset=SchoolClass.objects.all(),slug_field='name',)

    class Meta:
        model = Attendance
        fields = ['school_class', 'date', 'student', 'teacher', 'is_present']

class SchoolClassSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = SchoolClass
        fields = ['name', 'attendance']

    def get_attendance(self, obj):
        # Get all attendance records for the class, ordered by student and date
        attendance_qs = Attendance.objects.filter(school_class=obj).order_by('student', '-date')
        
        # Create a dictionary to store the latest attendance for each student
        latest_attendance = {}
        
        for attendance in attendance_qs:
            if attendance.student_id not in latest_attendance:
                latest_attendance[attendance.student_id] = attendance
        
        # Convert the dictionary values to a list
        latest_attendance_list = list(latest_attendance.values())
        
        return AttendanceSerializer(latest_attendance_list, many=True).data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    SchoolClass_data= serializers.SlugRelatedField( 
        queryset=SchoolClass.objects.all(),slug_field='name',)
    class Meta:
        model = Student
        fields = ['id', 'name','image','ago','adres','file_namber','father','SchoolClass_data','info','user']

class SchoolClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)  # تضمين الطلاب في السيريالايزر
    representative = TeacherSerializer(read_only=True) 
    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'students','representative']




class Grad_serializers(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_class = serializers.CharField(source='school_class.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()

    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        label="الطالب"
    )
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        label="المادة"
    )
    school_class = serializers.PrimaryKeyRelatedField(
        queryset=SchoolClass.objects.all(),
        label="الفصل"
    )

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'student_class', 'subject', 'subject_name', 'teacher_name', 'school_class', 'grade', 'final_grade', 'exam_name', 'date']

    def get_teacher_name(self, obj):
        teacher = obj.subject.teachers.first()
        return teacher.name if teacher else "غير محدد"

    def validate(self, data):
        if data['grade'] > data['final_grade']:
            raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
        return data   




from rest_framework import serializers

class BulkGradeSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    final_grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    exam_name = serializers.CharField(max_length=100)
    date = serializers.DateField(required=False)

    def validate(self, data):
        if data['grade'] > data['final_grade']:
            raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
        return data



# from rest_framework import serializers

# class FileUploadSerializer(serializers.Serializer):
#     file = serializers.FileField()  # حقل رفع ملف
# class Grad_serializers(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     student_class = serializers.CharField(source='school_class.name', read_only=True)  # عرض اسم الفصل
#     subject_name = serializers.CharField(source='subject.name', read_only=True)
#     teacher_name = serializers.SerializerMethodField()

#     student = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(),
#         label="الطالب"
#     )
#     subject = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(),
#         label="المادة"
#     )
#     school_class = serializers.PrimaryKeyRelatedField(
#         queryset=SchoolClass.objects.all(),
#         label="الفصل"  # إضافة الفصل في الـ Serializer
#     )

#     class Meta:
#         model = Grade
#         fields = ['id', 'student', 'student_name', 'student_class', 'subject', 'subject_name', 'teacher_name', 'school_class', 'grade', 'final_grade', 'exam_name', 'date']  # Include school_class

#     def get_teacher_name(self, obj):
#         teacher = obj.subject.teachers.first()  # Assuming the subject has multiple teachers
#         return teacher.name if teacher else "غير محدد"

#     def validate(self, data):
#         if data['grade'] > data['final_grade']:
#             raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         return data

# class Grad_serializers(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     student_class = serializers.CharField(source='student.schoolclass.name', read_only=True)  # عرض الفصل الذي ينتمي إليه الطالب
#     subject_name = serializers.CharField(source='subject.name', read_only=True)
#     teacher_name = serializers.SerializerMethodField()  # عرض اسم المدرس

#     student = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(),
#         label="الطالب"
#     )
#     subject = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(),
#         label="المادة"
#     )

#     class Meta:
#         model = Grade
#         fields = ['id', 'student', 'student_name', 'student_class', 'subject', 'subject_name', 'teacher_name', 'grade', 'final_grade', 'exam_name', 'date']  # Include new fields

#     def get_teacher_name(self, obj):
#         # إرجاع اسم المدرس الذي يدرس المادة
#         teacher = obj.subject.teachers.first()  # Assuming the subject has multiple teachers, we take the first one
#         return teacher.name if teacher else "غير محدد"

#     def validate(self, data):
#         if data['grade'] > data['final_grade']:
#             raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         return data


# class Grad_serializers(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     student_class = serializers.CharField(source='student.schoolclass.name', read_only=True)  # عرض الفصل الذي ينتمي إليه الطالب
#     subject_name = serializers.CharField(source='subject.name', read_only=True)
#     teacher_name = serializers.SerializerMethodField()  # عرض اسم المدرس

#     student = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(),
#         label="الطالب"
#     )
#     subject = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(),
#         label="المادة"
#     )

#     class Meta:
#         model = Grade
#         fields = ['id', 'student', 'student_name', 'student_class', 'subject', 'subject_name', 'teacher_name', 'grade', 'final_grade', 'exam_name', 'date']  # Include new fields

#     def get_teacher_name(self, obj):
#         # إرجاع اسم المدرس الذي يدرس المادة
#         teacher = obj.subject.teachers.first()  # Assuming the subject has multiple teachers, we take the first one
#         return teacher.name if teacher else "غير محدد"

#     def validate(self, data):
#         if data['grade'] > data['final_grade']:
#             raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         return data

# class Grad_serializers(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     student = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(),
#         label="الطالب"
#     )
#     subject_name = serializers.CharField(source='subject.name', read_only=True)
#     subject = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(),
#         label="المادة"
#     )

#     class Meta:
#         model = Grade
#         fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 'grade', 'final_grade', 'exam_name', 'date']  # Include new fields

#     def validate(self, data):
#         if data['grade'] > data['final_grade']:
#             raise serializers.ValidationError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         return data


############################################################################################


class Task_serializers(serializers.ModelSerializer):
    assigned_by_name = serializers.CharField(source='assigned_by.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_by', 'assigned_by_name', 'assigned_to', 'assigned_to_name', 'due_date', 'is_completed', 'Approved']


############################################################################################


class Task_Parents_serializers(serializers.ModelSerializer):

    student = serializers.SlugRelatedField(
        queryset=Student.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = info_to_Parent
        fields = ['id', 'student', 'task', 'image'] 



class TeacherSerializer(serializers.ModelSerializer):
    classes= serializers.SlugRelatedField( 
        queryset=SchoolClass.objects.all(),slug_field='name',)

    class Meta:
        model = Teacher
        fields = '__all__'  



class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = [ 'is_present'] 





class Teacher_now_AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = [ 'id','teacher','date','is_present'] 






class nowTeacherSerializer(serializers.ModelSerializer):
    classes = serializers.SlugRelatedField(
        queryset=SchoolClass.objects.all(), slug_field='name', many=True
    )
    subjects = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', many=True
    )
    class Meta:
        model = Teacher
        fields =  [ 'id','user','name','phon','image','is_class_representative','classes','subjects','notes'] 


class Subject_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'  

class InfoToParentSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        queryset=Student.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = info_to_Parent_by_class
        fields = ['student', 'task', 'image']

        
class Principal_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = '__all__'  


class event_all_Serializer(serializers.ModelSerializer):
    class Meta:
        model = event_to_all
        fields = '__all__'


class Class_schedule_Serializer(serializers.ModelSerializer):
    school_class = serializers.SlugRelatedField(
        queryset=SchoolClass.objects.all(), 
        slug_field='name'  # Removed many=True
    )

    teacher_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    def get_teacher_name(self, obj):
        return obj.teacher.name

    def get_subject_name(self, obj):
        return obj.subject.name


    class Meta:
        model = Schedule
        fields = '__all__'



class now_SchoolClassSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True)
    student_set = StudentSerializer(many=True)

    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'teachers', 'student_set']


# from rest_framework import serializers
# from .models import Schedule

# class ScheduleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Schedule
#         fields = '__all__'
# class AttendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attendance
#         fields = ['school_class', 'student', 'teacher', 'date', 'is_present']


# class Teacher_now_AttendanceSerializer(serializers.ModelSerializer):
#     teacher_name = serializers.CharField(source='teacher.name', read_only=True)
#     teacher_user = serializers.CharField(source='teacher.user.username', read_only=True)

#     class Meta:
#         model = TeacherAttendance
#         fields = ['teacher_name', 'teacher_user', 'date', 'is_present']



# class TeacherAttendance(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
#     date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField
#     is_present = models.BooleanField(default=False)




# class Task_Parents_serializers(serializers.ModelSerializer):
#     Parent = serializers.SerializerMethodField()

#     class Meta:
#         model = info_to_Parent
#         fields = ['id', 'Parent', 'task', 'image']


# from rest_framework import serializers
# from home.models import Attendance, SchoolClass

# class AttendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attendance
#         fields = ['school_class', 'date', 'student', 'teacher', 'is_present']

# class SchoolClassSerializer(serializers.ModelSerializer):
#     attendance = serializers.SerializerMethodField()

#     class Meta:
#         model = SchoolClass
#         fields = ['name', 'attendance']

#     def get_attendance(self, obj):
#         # Get the latest attendance records for the school class on a specific date
#         attendance_qs = Attendance.objects.filter(school_class=obj).order_by('student', '-date').distinct('student')
#         return AttendanceSerializer(attendance_qs, many=True).data
# class Grade(models.Model):
#     class Meta:
#         verbose_name_plural = " الدرجات"
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
#     grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
#     date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

#     def __str__(self):
#         return f"{self.student.name} - {self.subject.name} - {self.grade}"

# class Task(models.Model):
#     class Meta:
#         verbose_name_plural = "المهام"

#     title = models.CharField(max_length=255, verbose_name="عنوان المهمة")
#     description = models.TextField(verbose_name="وصف المهمة")
#     assigned_by = models.ForeignKey(Principal, on_delete=models.CASCADE, verbose_name="تم التكليف بواسطة")
#     assigned_to = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="تم التكليف إلى")
#     due_date = models.DateField(verbose_name="تاريخ الاستحقاق")
#     is_completed = models.BooleanField(default=False, verbose_name="تمت المهمة")

    # def __str__(self):
    #     return self.title
    