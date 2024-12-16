from django.contrib import admin
from.models import info_to_Parent,TeacherAttendance,info_to_Parent_by_class,event_to_all
# Register your models here.
admin.site.register(info_to_Parent)
admin.site.register(TeacherAttendance)
admin.site.register(info_to_Parent_by_class)
admin.site.register(event_to_all)