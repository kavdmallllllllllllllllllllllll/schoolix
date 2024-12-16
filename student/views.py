from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import StudentSerializer,GradeSerializer,ScheduleSerializer,ComplaintSerializer
from home.models import Student,Grade,Schedule
from.models import Complaint
#profile
class student_Profile_APIView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.groups.filter(name='Parents').exists():
            try:
                # Retrieve the Student instance associated with the current user
                student = Student.objects.get(user=user)
                return student
            except Student.DoesNotExist:
                raise PermissionDenied("Student profile not found.")
        else:
            raise PermissionDenied("You do not have permission to access this resource.")



#Grades
class StudentGradesAPIView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Parents').exists():
            try:
                student = Student.objects.get(user=user)
                return Grade.objects.filter(student=student)
            except Student.DoesNotExist:
                raise PermissionDenied("Student profile not found.")
        else:
            raise PermissionDenied("You do not have permission to access this resource.")


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from .serializers import ScheduleSerializer
#جدول الحصص
class StudentScheduleAPIView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Parents').exists():
            try:
                student = Student.objects.get(user=user)
                return Schedule.objects.filter(school_class=student.SchoolClass_data)
            except Student.DoesNotExist:
                raise PermissionDenied("Student profile not found.")
        else:
            raise PermissionDenied("You do not have permission to access this resource.")



class ComplaintListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter complaints to show only those created by the authenticated user
        return Complaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user field to the authenticated user
        serializer.save(user=self.request.user)

