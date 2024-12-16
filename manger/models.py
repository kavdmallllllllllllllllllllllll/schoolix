from django.db import models

# Create your models here.
from home.models import Student,SchoolClass
from home.models import Teacher
from django.db import models
from django.utils import timezone

# Create your models here.
class info_to_Parent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Parent")
    task=models.TextField()
    image = models.ImageField(upload_to='info_to_Parent/', null=True, blank=True)
    def __str__(self):
        return self.student.name
    


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['teacher', 'date']
        verbose_name = "Teacher Attendance"
        verbose_name_plural = "Teacher Attendance"

    def __str__(self):
        return f'- {self.date}'
    

class info_to_Parent_by_class(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Student")
    task = models.TextField()
    image = models.ImageField(upload_to='info_to_Parent/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField

    def __str__(self):
        return self.student.name if self.student else "No Student Assigned"
    

class event_to_all(models.Model):
    name=models.CharField(max_length=150)
    event_info=models.TextField()
    image = models.ImageField(upload_to='info_to_Parent/', null=True, blank=True)
    def __str__(self):
        return self.name
    