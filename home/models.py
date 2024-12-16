from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

# نموذج المدير
class Principal(models.Model):
    class Meta:
        verbose_name_plural = "المدير"
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)

    def __str__(self):
        return self.name

    def create_class(self, class_name):
        # إنشاء فصل جديد وتضمين جميع الطلاب فيه
        new_class = SchoolClass.objects.create(name=class_name)
        students = Student.objects.all()
        new_class.student_set.add(*students)
        return new_class

# نموذج ولي الأمر
class Parent(models.Model):
    class Meta:
        verbose_name_plural = "ولي الامر"
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
    name = models.CharField(max_length=150)
    children = models.ManyToManyField('Student', related_name="parents", verbose_name="الطلاب")

    def __str__(self):
        return self.name

# نموذج المدرس
class Teacher(models.Model):
    class Meta:
        verbose_name_plural = " المدرس"
    user = models.OneToOneField(User, null=True, blank=True , on_delete=models.CASCADE, verbose_name="اسم المستخدم")
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
    is_class_representative = models.BooleanField(default=False)
    classes = models.ManyToManyField('SchoolClass', related_name="teachers", verbose_name="الفصول")
    subjects = models.ManyToManyField('Subject', related_name="teachers", verbose_name="المواد")
    phon= models.CharField(max_length=150, verbose_name="رقم الهاتف ", null=True, blank=True)
    notes=models.TextField( null=True, blank=True)
    def __str__(self):
        return self.name

    def generate_unique_username(self, base_username):
        """Generate a unique username by appending numbers if necessary."""
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        return username

    def save(self, *args, **kwargs):
        # Create or update user when saving teacher
        if self.user is None:
            # Generate a unique username
            unique_username = self.generate_unique_username(self.name)
            # Create the user with a unique username and hashed phone number as password
            self.user = User.objects.create(
                username=unique_username,
                password=make_password(self.phon),
            )
        else:
            # If user exists, update username
            self.user.username = self.generate_unique_username(self.name)

            # Update password only if the user doesn't have a password set
            if not self.user.has_usable_password() and self.phon:
                self.user.password = make_password(self.phon)

            self.user.save()

        super().save(*args, **kwargs)  # Save the teacher after user creation or update

        # Add the teacher to the 'teacher' group if not already added
        teacher_group, created = Group.objects.get_or_create(name='teacher')
        if self.user and not self.user.groups.filter(name='teacher').exists():
            self.user.groups.add(teacher_group)

    # def generate_unique_username(self, base_username):
    #     """Generate a unique username by appending numbers if necessary."""
    #     username = base_username
    #     counter = 1
    #     while User.objects.filter(username=username).exists():
    #         username = f"{base_username}_{counter}"
    #         counter += 1
    #     return username

    # def save(self, *args, **kwargs):
    #     # Create or update user when saving teacher
    #     if self.user is None:
    #         # Generate a unique username
    #         unique_username = self.generate_unique_username(self.name)
    #         # Create the user with a unique username and hashed phone number as password
    #         self.user = User.objects.create(
    #             username=unique_username,
    #             password=make_password(self.phon),
    #         )
    #     else:
    #         # If user exists, update username and password if necessary
    #         self.user.username = self.generate_unique_username(self.name)
    #         if self.phon:  # Update password if phone number is available
    #             self.user.password = make_password(self.phon)
    #         self.user.save()

    #     super().save(*args, **kwargs)  # Save the teacher after user creation or update

    #     # Add the teacher to the 'teacher' group if not already added
    #     teacher_group, created = Group.objects.get_or_create(name='teacher')
    #     if self.user and not self.user.groups.filter(name='teacher').exists():
    #         self.user.groups.add(teacher_group)
# نموذج المادة الدراسية
class Subject(models.Model):
    class Meta:
        verbose_name_plural = " المادةالدرسية"
    name = models.CharField(max_length=150, verbose_name="اسم المادة")

    def __str__(self):
        return self.name

# نموذج الفصل الدراسي
class SchoolClass(models.Model):
    class Meta:
        verbose_name_plural = "الفصل"
    name = models.CharField(max_length=150)
    representative = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_class_representative': True})

    def __str__(self):
        return self.name

    def add_students(self, students):
        # إضافة طلاب إلى الفصل
        self.students.add(*students)


# نموذج الطالب
class Student(models.Model):
    class Meta:
        verbose_name_plural = " الطالب"
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
    ago = models.CharField(max_length=150, verbose_name="السن")
    adres = models.TextField(verbose_name="عنوان السكن")
    file_namber = models.CharField(max_length=150, verbose_name="رقم الملف")
    father = models.CharField(max_length=150, verbose_name="اسم ولي الأمر")
    father_nammber = models.CharField(max_length=150, verbose_name="رقم ولي الأمر")
    SchoolClass_data = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
    info = models.TextField(verbose_name="ملحوظات عامة", null=True, blank=True)
    mother_name = models.CharField(max_length=150, verbose_name="اسم الام")
    mother_number = models.CharField(max_length=150, verbose_name="رقم الام")
    device_number = models.CharField(max_length=150, verbose_name="رقم الجهاز",null=True,blank=True)  # New field for device number

    GENDER_CHOICES = [
        ('male', 'male'),
        ('feminine', 'feminine'),
    ]
    gender = models.CharField(max_length=150, choices=GENDER_CHOICES, verbose_name="الجنس", null=True, blank=True)

    def __str__(self):
        return self.name
    

    def generate_unique_username(self, base_username):
        """Generate a unique username by appending numbers if necessary."""
        username = base_username
        counter = 1
        # Ensure the username is unique by appending a number if it already exists
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        return username

    def save(self, *args, **kwargs):
        # التأكد من أن `mother_number` و `father_nammber` من النوع `str`
        father_number_str = str(self.father_nammber) if self.father_nammber else ""
        mother_number_str = str(self.mother_number) if self.mother_number else ""

        # إنشاء أو تحديث المستخدم عند حفظ الطالب
        if self.user is None:
            # توليد اسم مستخدم فريد بناءً على رقم ولي الأمر
            unique_username = self.generate_unique_username(father_number_str)
            # إنشاء المستخدم مع اسم مستخدم فريد، والبريد الإلكتروني كرقم الأب، وكلمة المرور كرقم الأم
            self.user = User.objects.create(
                username=unique_username,
                email=father_number_str,  # تعيين البريد الإلكتروني كرقم الأب
                password=make_password(mother_number_str)  # تعيين كلمة المرور كرقم الأم
            )
        else:
            # إذا كان المستخدم موجودًا، تحديث اسم المستخدم والبريد الإلكتروني
            self.user.username = self.generate_unique_username(father_number_str)
            self.user.email = father_number_str  # تحديث البريد الإلكتروني ليكون رقم الأب

            # تحديث كلمة المرور فقط إذا لم يكن لديه كلمة مرور قابلة للاستخدام
            if not self.user.has_usable_password() and mother_number_str:
                self.user.password = make_password(mother_number_str)
            
            self.user.save()

        super(Student, self).save(*args, **kwargs)

        # Add the student's parent to the 'Parents' group if not already added
        parents_group, created = Group.objects.get_or_create(name='Parents')
        if self.user and not self.user.groups.filter(name='Parents').exists():
            self.user.groups.add(parents_group)

# نموذج الطالب
# class Student(models.Model):
#     class Meta:
#         verbose_name_plural = " الطالب"
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
#     name = models.CharField(max_length=150)
#     image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
#     ago = models.CharField(max_length=150, verbose_name="السن")
#     adres = models.TextField(verbose_name="عنوان السكن")
#     file_namber = models.CharField(max_length=150, verbose_name="رقم الملف")
#     father = models.CharField(max_length=150, verbose_name="اسم ولي الأمر")
#     father_nammber = models.CharField(max_length=150, verbose_name="رقم ولي الأمر")
#     SchoolClass_data = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
#     info = models.TextField(verbose_name="ملحوظات عامة", null=True, blank=True)
#     birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")  # New field for birth date
#     mother_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="اسم الام")
#     mother_number = models.CharField(max_length=150, null=True, blank=True, verbose_name="رقم الام")

#     GENDER_CHOICES = [
#         ('male', 'male'),
#         ('feminine', 'feminine'),
#     ]
#     gender = models.CharField(max_length=150, choices=GENDER_CHOICES, verbose_name="الجنس", null=True, blank=True)

#     def __str__(self):
#         return self.name
#     def generate_unique_username(self, base_username):
#         """Generate a unique username by appending numbers if necessary."""
#         username = base_username
#         counter = 1
#         # Ensure the username is unique by appending a number if it already exists
#         while User.objects.filter(username=username).exists():
#             username = f"{base_username}_{counter}"
#             counter += 1
#         return username

#     def save(self, *args, **kwargs):
#         # إذا كان المستخدم None، يتم إنشاء مستخدم جديد
#         if self.user is None:
#             # Generate a unique username based on student's name
#             unique_username = self.generate_unique_username(self.name)
#             # Create the user with a unique username and the father's phone number as password
#             self.user = User.objects.create(
#                 username=unique_username,
#                 password=make_password(self.father_nammber),  # Using father's phone number as the password
#             )

#             super().save(*args, **kwargs)  # Save the student after user creation
#         else:
#             # إذا كان المستخدم موجودًا، لا يتم تحديث أي بيانات
#             super().save(*args, **kwargs)  # Save the student without changing user data

#         # Add the student's parent to the 'Parents' group if not already added
#         parents_group, created = Group.objects.get_or_create(name='Parents')
#         if self.user and not self.user.groups.filter(name='Parents').exists():
#             self.user.groups.add(parents_group)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Student)
def delete_user_with_student(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()


    # Method to generate a unique username
    # def generate_unique_username(self, base_username):
    #     """Generate a unique username by appending numbers if necessary."""
    #     username = base_username
    #     counter = 1
    #     # Ensure the username is unique by appending a number if it already exists
    #     while User.objects.filter(username=username).exists():
    #         username = f"{base_username}_{counter}"
    #         counter += 1
    #     return username

    # def save(self, *args, **kwargs):
    #     # Create or update user when saving student
    #     if self.user is None:
    #         # Generate a unique username based on student's name
    #         unique_username = self.generate_unique_username(self.name)
    #         # Create the user with a unique username and the father's phone number as password
    #         self.user = User.objects.create(
    #             username=unique_username,
    #             password=make_password(self.father_nammber),  # Using father's phone number as the password
    #         )
    #     else:
    #         # If user exists, update username and password if necessary
    #         self.user.username = self.generate_unique_username(self.name)
    #         if self.father_nammber:  # Update password if father's phone number is available
    #             self.user.password = make_password(self.father_nammber)
    #         self.user.save()

    #     super().save(*args, **kwargs)  # Save the student after user creation or update

    #     # Add the student's parent to the 'Parents' group if not already added
    #     parents_group, created = Group.objects.get_or_create(name='Parents')
    #     if self.user and not self.user.groups.filter(name='Parents').exists():
    #         self.user.groups.add(parents_group)







class Grade(models.Model):
    class Meta:
        verbose_name_plural = "الدرجات"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name="الفصل",null=True,blank=True)  # إضافة حقل الفصل
    grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة النهائية")
    exam_name = models.CharField(max_length=100, verbose_name="اسم الامتحان")
    date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

    def save(self, *args, **kwargs):
        if self.grade > self.final_grade:
            raise ValueError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.exam_name} - {self.grade}/{self.final_grade}"





# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class BulkGradeCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         school_class_id = request.data.get('school_class_id')
#         if not school_class_id:
#             return Response({"error": "يرجى تحديد الفصل"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             school_class = SchoolClass.objects.get(id=school_class_id)
#         except SchoolClass.DoesNotExist:
#             return Response({"error": "الفصل غير موجود"}, status=status.HTTP_404_NOT_FOUND)

#         grades_data = request.data.get('grades', [])
#         serializer = BulkGradeSerializer(data=grades_data, many=True)
#         if serializer.is_valid():
#             for grade_data in serializer.validated_data:
#                 student_id = grade_data['student_id']
#                 try:
#                     student = Student.objects.get(id=student_id)
#                 except Student.DoesNotExist:
#                     return Response(
#                         {"error": f"الطالب بالرقم {student_id} غير موجود"},
#                         status=status.HTTP_404_NOT_FOUND,
#                     )

#                 Grade.objects.create(
#                     student=student,
#                     school_class=school_class,
#                     subject=Subject.objects.first(),  # اختر المادة الافتراضية
#                     grade=grade_data['grade'],
#                     final_grade=grade_data['final_grade'],
#                     exam_name=grade_data['exam_name'],
#                     date=grade_data.get('date', timezone.now()),
#                 )

#             return Response({"message": "تمت إضافة الدرجات بنجاح"}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {
#     "school_class_id": 1,
#     "grades": [
#         {
#             "student_id": 101,
#             "grade": 85.5,
#             "final_grade": 100,
#             "exam_name": "امتحان نهاية الفصل"
#         },
#         {
#             "student_id": 102,
#             "grade": 90.0,
#             "final_grade": 100,
#             "exam_name": "امتحان نهاية الفصل"
#         }
#     ]
# }




# class Grade(models.Model):
#     class Meta:
#         verbose_name_plural = "الدرجات"

#     student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
#     grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
#     final_grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة النهائية")  # New field
#     exam_name = models.CharField(max_length=100, verbose_name="اسم الامتحان")  # New field
#     date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

#     def save(self, *args, **kwargs):
#         if self.grade > self.final_grade:
#             raise ValueError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.name} - {self.subject.name} - {self.exam_name} - {self.grade}/{self.final_grade}"
# class Grade(models.Model):
#     class Meta:
#         verbose_name_plural = "الدرجات"

#     student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
#     grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
#     final_grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة النهائية")  # New field
#     exam_name = models.CharField(max_length=100, verbose_name="اسم الامتحان")  # New field
#     date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

#     def save(self, *args, **kwargs):
#         if self.grade > self.final_grade:
#             raise ValueError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.name} - {self.subject.name} - {self.exam_name} - {self.grade}/{self.final_grade}"

# نموذج الدرجات
# class Grade(models.Model):
#     class Meta:
#         verbose_name_plural = " الدرجات"
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
#     grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
#     date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

#     def __str__(self):
#         return f"{self.student.name} - {self.subject.name} - {self.grade}"
# class Grade(models.Model):
#     class Meta:
#         verbose_name_plural = "الدرجات"

#     student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
#     grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
#     final_grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة النهائية")  # New field
#     exam_name = models.CharField(max_length=100, verbose_name="اسم الامتحان")  # New field
#     date = models.DateField(default=timezone.now, verbose_name="تاريخ إدخال الدرجة")

#     def save(self, *args, **kwargs):
#         if self.grade > self.final_grade:
#             raise ValueError("لا يمكن أن تكون الدرجة أعلى من الدرجة النهائية")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.name} - {self.subject.name} - {self.exam_name} - {self.grade}/{self.final_grade}"









# نموذج الحضور
class Attendance(models.Model):
    class Meta:
        verbose_name_plural = " الغياب"
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)

    # class Meta:
    #     unique_together = ('school_class', 'date', 'student')

    def __str__(self):
        return f"{self.student.name} - {self.school_class.name} - {self.date}"

    @staticmethod
    def get_absence_rate(student, start_date, end_date):
        # Fetch all attendance records for the student between the start and end date
        total_days = Attendance.objects.filter(
            student=student, 
            date__range=[start_date, end_date]
        ).count()

        # Count the days the student was absent
        absent_days = Attendance.objects.filter(
            student=student, 
            is_present=False,
            date__range=[start_date, end_date]
        ).count()

        # Calculate the absence rate
        absence_rate = (absent_days / total_days) * 100 if total_days > 0 else 0
        return absence_rate    

class Task(models.Model):
    class Meta:
        verbose_name_plural = "المهام"

    title = models.CharField(max_length=255, verbose_name="عنوان المهمة")
    description = models.TextField(verbose_name="وصف المهمة")
    assigned_by = models.ForeignKey(Principal, on_delete=models.CASCADE, verbose_name="تم التكليف بواسطة")
    assigned_to = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="تم التكليف إلى")
    due_date = models.DateField(verbose_name="تاريخ الاستحقاق")
    is_completed = models.BooleanField(default=False, verbose_name="تمت المهمة")
    Approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# نموذج جدول الحصص
class Schedule(models.Model):
    class Meta:
        verbose_name_plural = "جداول الحصص"
    name=models.CharField(max_length=180)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name="الفصل")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="اسم المدرس")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
    start_time = models.TimeField(verbose_name="وقت بدء الحصة",null=True,blank=True)
    end_time = models.TimeField(verbose_name="وقت انتهاء الحصة",null=True,blank=True)
    day_of_week = models.CharField(max_length=9, choices=[
        ('Saturday', 'السبت'),
        ('Sunday', 'الأحد'),
        ('Monday', 'الاثنين'),
        ('Tuesday', 'الثلاثاء'),
        ('Wednesday', 'الأربعاء'),
        ('Thursday', 'الخميس'),
        ('Friday', 'الجمعة')
    ], verbose_name="يوم الأسبوع")

    def __str__(self):
        return f"{self.school_class.name} - {self.subject.name} - {self.day_of_week} - {self.start_time} to {self.end_time}"

# إشارة لإنشاء توكن عند إنشاء مستخدم جديد
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
