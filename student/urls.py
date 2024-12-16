from django.urls import path
from .views import student_Profile_APIView, StudentGradesAPIView, StudentScheduleAPIView,ComplaintListCreateAPIView

urlpatterns = [
    path('', student_Profile_APIView.as_view(), name="student_Profile_APIView"),
    path('Grades/', StudentGradesAPIView.as_view(), name="StudentGradesAPIView"),
    path('Student_Schedule/', StudentScheduleAPIView.as_view(), name="StudentScheduleAPIView"),
    path('complaints/', ComplaintListCreateAPIView.as_view(), name='complaint-list-create'),

]
