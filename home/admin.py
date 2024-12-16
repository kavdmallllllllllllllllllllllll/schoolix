from django.contrib import admin
from.models import Student,Teacher,Attendance,SchoolClass,Grade,Subject,Task,Schedule
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Attendance)
admin.site.register(SchoolClass)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(Schedule)

from django.contrib import admin
from .models import Principal, SchoolClass

@admin.action(description='إنشاء فصل جديد وإضافة جميع الطلاب')
def create_class_action(modeladmin, request, queryset):
    for principal in queryset:
        new_class = principal.create_class("Class A")
        modeladmin.message_user(request, f"تم إنشاء الفصل {new_class.name} بنجاح وإضافة {new_class.student_set.count()} طلاب.")

class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    actions = [create_class_action]

admin.site.register(Principal, PrincipalAdmin)
