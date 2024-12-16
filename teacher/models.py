from django.db import models
from home.models import SchoolClass,Student,Teacher
from django.utils import timezone

# Create your models here.
class Academic_tasks(models.Model):
    name=models.CharField(max_length=180)
    task=models.TextField()
    schoolclass = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفصل")
    image = models.ImageField(upload_to='user/profile/Academic_tasks', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField



class leve_student(models.Model):
    class Meta:
        verbose_name_plural = "خروج نصف يوم"
    
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name="الفصل",null=True,blank=True,)
    date = models.DateTimeField(default=timezone.now, verbose_name="التاريخ")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="المعلم")
    is_present = models.BooleanField(default=True, verbose_name="حاضر")
    # Adding more detailed fields for permissions and reasons for absence
    permission_type = models.CharField(
        max_length=50,
        choices=[
            ('بدون إذن', 'بدون إذن'),
            ( 'نصف يوم', 'نصف يوم'),
            ('إجازة بعذر', 'إجازة بعذر'),
            ('إجازة طبية', 'إجازة طبية'),
            ('حالة طارئة', 'حالة طارئة'),
            ('سبب آخر', 'سبب آخر')
        ],
        default='none',
        verbose_name="نوع الإذن"
    )
    
    reason = models.TextField(
        null=True,
        blank=True,
        verbose_name="سبب الغياب/الإذن"
    )
    
    permission_start_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="وقت بدء الإذن"
    )
    
    permission_end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="وقت انتهاء الإذن"
    )

    def __str__(self):
        status = "حاضر" if self.is_present else "غائب"
        permission = f" - إذن: {self.get_permission_type_display()}" if self.permission_type != 'none' else ""
        return f"{self.student.name} - {status}{permission} - {self.date.strftime('%Y-%m-%d')}"

