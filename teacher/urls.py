from django.urls import path
from. import views
from .views import (
    TeacherTaskUpdateView, 
    TeacherTaskListView,
    SchoolClassStudentsAPIView,
    SchoolClassAttendanceToggleAPIView,
    SchoolClassListAPIView,
    # SchoolClassAttendance2CreateAPIView,
    TeacherProfileAPIView,HomeWorkStudentView,TeacherAttendanceListCreateView,
    leave_student
)
urlpatterns = [
    path('task/', TeacherTaskListView.as_view(), name='task-list'),  # لعرض قائمة المهام
    path('task/<int:pk>/', TeacherTaskUpdateView.as_view(), name='task-update'),
    
    path('school_class/', SchoolClassListAPIView.as_view(), name='school_class_list'),
    path('school_class/<int:pk>/', SchoolClassStudentsAPIView.as_view(), name='school_class_students'),


    path('school_class/<int:pk>/attendance/', SchoolClassAttendanceToggleAPIView.as_view(), name='school_class_attendance'),

    # path('school_class/<int:pk>/attendance2/', SchoolClassAttendance2CreateAPIView.as_view(), name='school_class_attendance2'),
    path('profile/', TeacherProfileAPIView.as_view(), name='teacher-profile'),
    path('',HomeWorkStudentView.as_view(),name='home_work_Student'),
    path('Teacher_Attendanc/',TeacherAttendanceListCreateView.as_view(),name="TeacherAttendanceListCreateView"),

    path('api/leave-students/', leave_student.as_view(), name='leave-students-list'),

]
