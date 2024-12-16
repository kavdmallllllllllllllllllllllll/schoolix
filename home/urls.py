from .import views
from django.urls import path 
from.views import PrincipalListCreateView,refresh_token

from .views import StudentListInClassView, AttendanceCreateView,ManagerAddTaskView
from .views import ManagerAddTaskView

urlpatterns = [
    path('', views.home, name='home'),
    path('add-task/', ManagerAddTaskView.as_view(), name='manager-add-task'),

    path('p/', PrincipalListCreateView.as_view(), name='PrincipalListCreateView'),
    path('api/refresh-token/', refresh_token, name='refresh_token'),

    path('classes/<int:class_id>/students/', StudentListInClassView.as_view(), name='student-list-in-class'),
    path('attendance/', AttendanceCreateView.as_view(), name='attendance-create'),
]
