
from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")  # Changed to ForeignKey
    name = models.CharField(max_length=150, verbose_name="الاسم")
    text = models.TextField(verbose_name="ملحوظات عامة", null=True, blank=True)
    reviewed = models.BooleanField(default=False, verbose_name="تم المراجعة")
    
    class Meta:
        verbose_name = "شكوى"
        verbose_name_plural = "شكاوى"
    
    def __str__(self):
        return f"{self.name} - {self.user}"


# class Student(models.Model):
#     class Meta:
#         verbose_name_plural = " الطالب"
#     user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, verbose_name="اسم المستخدم")
#     name = models.CharField(max_length=150)
#     image = models.ImageField(upload_to='user/profile', verbose_name="صورة شخصية -", null=True, blank=True)
#     ago = models.CharField(max_length=150, verbose_name="السن")
#     adres = models.TextField(verbose_name="عنوان السكن")
#     file_namber = models.CharField(max_length=150, verbose_name="رقم الملف")
#     father = models.CharField(max_length=150, verbose_name="اسم ولي الأمر")
#     father_nammber = models.CharField(max_length=150, verbose_name="رقم ولي الأمر")
#     SchoolClass_data = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
#     info = models.TextField(verbose_name="ملحوظات عامة", null=True, blank=True)
#     mother_name = models.CharField(max_length=150, verbose_name="اسم الام")
#     mother_number = models.CharField(max_length=150, verbose_name="رقم الام")
    
#     GENDER_CHOICES = [
#         ('male', 'male'),
#         ('feminine', 'feminine'),
#     ]
#     gender = models.CharField(max_length=150, choices=GENDER_CHOICES, verbose_name="الجنس", null=True, blank=True)

#     def __str__(self):
#         return self.name