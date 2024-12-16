from .import views
from django.urls import path 
from .views import DailyAttendanceView, SchoolClassAttendanceView,SchoolClassListCreateView,SchoolClassDetailView,GenerateSongView

from.views import SchoolClass_Test_ListCreateView,StudentListView,GradeCreateView,task_CreateView,add_masssging_perns_CreateView,add_masssging_perns_int,Student_Test_ListCreateView,Teacher_Test_ListCreateView

from .views import attendance_report ,now_SchoolClassDetailView
from .views import SendTaskToClassView,SendTaskToClassView,mangerProfileAPIView,event_to_All_ListCreateView,Class_schedule_ListCreateView
from . import views  # تأكد من استيراد الدوال من ملف views
from .views import UpdateAttendanceStatusView,BulkGradeCreateView,RecordAttendanceAPIView

urlpatterns = [
    path('SchoolClass-count/',views.home_api_cont,name="home_api_cont"),
    path('teacher_profiles/', views.teacher_profiles_data, name='teacher_profiles_data'),

    path('SchoolClass/',SchoolClassListCreateView.as_view(),name="school_add_and_get"),
    path('SchoolClass/<int:pk>',SchoolClassDetailView.as_view(),name="SchoolClassDetailView"),

    path('attendance/daily/', DailyAttendanceView.as_view(), name='daily-attendance'),
    path('attendance/school-class/<int:school_class_id>/', SchoolClassAttendanceView.as_view(), name='school-class-attendance'),

    path('classes/', SchoolClass_Test_ListCreateView.as_view(), name='schoolclass-list-create'),
    path('classes/<int:school_class>/students/', StudentListView.as_view(), name='student-list'),
    path('grades/', GradeCreateView.as_view(), name='grade-create'),
    path('task/', task_CreateView.as_view(), name='task_CreateView'),
    path('A_message_to_parents/', add_masssging_perns_CreateView.as_view(), name='add_masssging_perns_CreateView'),
    path('A_message_to_parents/<int:pk>/', add_masssging_perns_int.as_view(), name='add_masssging_perns_int'),

    path('api/attendance_report/', attendance_report, name='attendance_report'),

    path('attendance/statistics/<int:school_class>/',views.attendance_statistics, name='attendance-statistics'),
    path('search_student_attendance/',views.search_student_attendance, name='search_student_attendance-statistics'),

    path('ai/', GenerateSongView.as_view(), name='GenerateSongView'),
    path('Student_Test_ListCreateView/', Student_Test_ListCreateView.as_view(), name='Student_Test_ListCreateView'),
    path('Teacher_Test_ListCreateView/', Teacher_Test_ListCreateView.as_view(), name='Teacher_Test_ListCreateView'),

    path('teacher_attendance_statistics/<int:teacher_id>/',views.teacher_attendance_statistics, name='teacher_attendance_statistics'),

    # path('api/send-task-to-class/<int:class_id>/', views.send_task_to_students, name='send_task_to_class'),
    path('api/send-task-to-class/<int:class_id>/', SendTaskToClassView.as_view(), name='send_task_to_class'),

    #path('api/list-tasks-by-class/<int:class_id>/', SendTaskToClassView.as_view(), name='list_tasks_by_class'),
    path('profile/', mangerProfileAPIView.as_view(), name='mangerProfileAPIView'),
    path('event/', event_to_All_ListCreateView.as_view(), name='event_to_All_ListCreateView'),
    path('Class-schedule/', Class_schedule_ListCreateView.as_view(), name='Class_schedule_ListCreateView'),

    path('class/<int:pk>/', now_SchoolClassDetailView.as_view(), name='class-detail'),


    path('import-students/', views.import_students_from_excel, name='import_students'),  # إضافة رابط الصفحة
    path('upload_attendance/', views.upload_attendance, name='upload_attendance'),  # إضافة رابط الصفحة

    path('api/update-attendance/<int:pk>/', UpdateAttendanceStatusView.as_view(), name='update_attendance_status'),
    path('grades-by_class/', BulkGradeCreateView.as_view(), name='BulkGradeCreateView'),

    path('RecordAttendanceAPIView/', RecordAttendanceAPIView.as_view(), name='RecordAttendanceAPIView'),


]
