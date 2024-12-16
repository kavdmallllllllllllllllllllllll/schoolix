from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render
from home.models import Student,Attendance,Principal,SchoolClass,Grade,Task,Teacher,Subject
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from home.serializers import PrincipalSerializer
from.serializers import StudentSerializer,AttendanceSerializer,SchoolClassSerializer,TeacherSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import SchoolClassSerializer, StudentSerializer,StudentSerializer,Grad_serializers,Task_serializers,Task_Parents_serializers,TeacherSerializer,TeacherAttendanceSerializer
from rest_framework.views import APIView
from django.utils import timezone
from collections import defaultdict
from.models import info_to_Parent,TeacherAttendance
from home.serializers import PrincipalSerializer
from django.utils import timezone
from django.db.models import Q
from django.utils import timezone
# from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api_cont(request):
    if request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='teacher').exists():
        if request.method == 'GET':
            today = timezone.now().date()

            # Fetch all students and attendance records for today
            principal_data = Student.objects.all()
            attendance_today = Attendance.objects.filter(date__date=today)

            # Serialize student data
            student_serializer = StudentSerializer(principal_data, many=True)
            students_count = Student.objects.count()

            # Collect names and counts of students who are present and absent today
            present_students = attendance_today.filter(is_present=True).values('student__id', 'student__name')
            absent_students = attendance_today.filter(is_present=False).values('student__id', 'student__name')
            present_count = present_students.count()
            absent_count = absent_students.count()

            # Find students with no attendance record for today
            students_with_attendance_today = attendance_today.values_list('student__id', flat=True)
            students_not_marked_today = principal_data.exclude(id__in=students_with_attendance_today).values('id', 'name')

            # Prepare attendance summary for each student
            students_attendance_data = []
            for student in principal_data:
                total_absent_days = Attendance.objects.filter(student=student, is_present=False).count()
                total_attendance_rate = Attendance.objects.filter(student=student, is_present=True).count()
                students_attendance_data.append({
                    'id': student.id,
                    'name': student.name,
                    'father_name': student.father,
                    'father_number': student.father_nammber,
                    'image': student.image.url if student.image else None,
                    'info': student.info,
                    'absent_days': total_absent_days,
                    'total_attendance_rate': total_attendance_rate
                })

            # Prepare teacher data with total absence count
            teachers = Teacher.objects.all()
            teachers_data = []
            for teacher in teachers:
                total_absent_days = TeacherAttendance.objects.filter(teacher=teacher, is_present=False).count()
                teacher_data = TeacherSerializer(teacher).data
                teacher_data['total_absent_days'] = total_absent_days
                teachers_data.append(teacher_data)

            # Teacher attendance counts for today
            teachers_present_today = TeacherAttendance.objects.filter(
                date__date=today, is_present=True).count()
            teachers_absent_today = TeacherAttendance.objects.filter(
                date__date=today, is_present=False).count()

            # Prepare the response data
            response_data = {
                'Teachers': teachers_data,
                'Total_Students': students_count,
                'Total_Present_Students_Today': present_count,
                'Total_Absent_Students_Today': absent_count,
                'principal_data': student_serializer.data,
                'present_students_today': list(present_students),
                'absent_students_today': list(absent_students),
                'attendance_name': students_attendance_data,
                'teachers_present_today': teachers_present_today,
                'teachers_absent_today': teachers_absent_today,
                'students_not_marked_today': list(students_not_marked_today)
            }

            return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)





class UpdateAttendanceStatusView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # تغيير حالة الحضور: إذا كان حاضر يصبح غائب والعكس
        instance.is_present = not instance.is_present
        instance.save()

        return Response({
            "student_id": instance.student.id,
            "student_name": instance.student.name,
            "is_present": instance.is_present,
        }, status=status.HTTP_200_OK)











# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='teacher').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()

#             # Fetch all students and attendance records for today
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today)

#             # Serialize student data
#             student_serializer = StudentSerializer(principal_data, many=True)
#             students_count = Student.objects.count()

#             # Collect names and counts of students who are present and absent today
#             present_students = attendance_today.filter(is_present=True).values('student__id', 'student__name')
#             absent_students = attendance_today.filter(is_present=False).values('student__id', 'student__name')
#             present_count = present_students.count()
#             absent_count = absent_students.count()

#             # Prepare attendance summary for each student
#             students_attendance_data = []
#             for student in principal_data:
#                 total_absent_days = Attendance.objects.filter(student=student, is_present=False).count()
#                 Total_attendance_rate=Attendance.objects.filter(student=student, is_present=True).count()
#                 students_attendance_data.append({
#                     'id': student.id,
#                     'name': student.name,
#                     'father_name': student.father,
#                     'father_number': student.father_nammber,
#                     'image': student.image.url if student.image else None,
#                     'info': student.info,
#                     'absent_days': total_absent_days,
#                     'Total_attendance_rate':Total_attendance_rate
                    
#                 })

#             # Prepare teacher data with total absence count
#             teachers = Teacher.objects.all()
#             teachers_data = []
#             for teacher in teachers:
#                 total_absent_days = TeacherAttendance.objects.filter(teacher=teacher, is_present=False).count()
#                 teacher_data = TeacherSerializer(teacher).data
#                 teacher_data['total_absent_days'] = total_absent_days
#                 teachers_data.append(teacher_data)

#             # Teacher attendance counts for today
#             teachers_present_today = TeacherAttendance.objects.filter(
#                 date__date=today, is_present=True).count()
#             teachers_absent_today = TeacherAttendance.objects.filter(
#                 date__date=today, is_present=False).count()

#             # Prepare the response data
#             response_data = {
#                 'Teachers': teachers_data,
#                 'Total_Students': students_count,
#                 'Total_Present_Students_Today': present_count,
#                 'Total_Absent_Students_Today': absent_count,
#                 'principal_data': student_serializer.data,
#                 'present_students_today': list(present_students),
#                 'absent_students_today': list(absent_students),
#                 'attendance_name': students_attendance_data,
#                 'teachers_present_today': teachers_present_today,
#                 'teachers_absent_today': teachers_absent_today
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response({"detail": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()

#             # Fetch data
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             students_count = Student.objects.count()
#             teachers = Teacher.objects.all()

#             # Serialize student data
#             student_serializer = StudentSerializer(principal_data, many=True)

#             # Calculate days absent for each student
#             students_attendance_data = []
#             for student in principal_data:
#                 total_absent_days = Attendance.objects.filter(student=student, is_present=False).count()
#                 students_attendance_data.append({
#                     'id':student.id,
#                     'name': student.name,
#                     'father_name': student.father,  # Use 'father' instead of 'father_name'
#                     'father_number': student.father_nammber,  # Use 'father_nammber' instead of 'father_number'
#                     'image': student.image.url if student.image else None,
#                     'info': student.info,
#                     'absent_days': total_absent_days
#                 })

#             # Prepare teacher data with total absence count
#             teachers_data = []
#             for teacher in teachers:
#                 total_absent_days = TeacherAttendance.objects.filter(teacher=teacher, is_present=False).count()
#                 teacher_data = TeacherSerializer(teacher).data
#                 teacher_data['total_absent_days'] = total_absent_days  # Add total absent days
#                 teachers_data.append(teacher_data)

#             # Teacher attendance counts for today
#             teachers_present_today = TeacherAttendance.objects.filter(
#                 date__date=today, is_present=True).count()
#             teachers_absent_today = TeacherAttendance.objects.filter(
#                 date__date=today, is_present=False).count()

#             # Prepare the response data
#             response_data = {
#                 'Teachers': teachers_data,
#                 'Students': students_count,
#                 'principal_data': student_serializer.data,
#                 'absent_student_days': attendance_today,
#                 'absent_student_name': list(name_data.values(
#                     'student__name', 'is_present', 'school_class__name',
#                     'teacher__name', 'student__father',
#                     'student__father_nammber', 'student__image', 'student__info'
#                 )),
#                 'attendance_name': students_attendance_data,  
#                 'teachers_present_today': teachers_present_today,
#                 'teachers_absent_today': teachers_absent_today
#             }

#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()

#             # Fetch data
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             students_count = Student.objects.count()
#             teachers = Teacher.objects.all()

#             # Serialize data
#             student_serializer = StudentSerializer(principal_data, many=True)
#             teacher_serializer = TeacherSerializer(teachers, many=True)

#             # Calculate days absent for each student
#             students_attendance_data = []
#             for student in principal_data:
#                 total_absent_days = Attendance.objects.filter(student=student, is_present=True).count()
#                 students_attendance_data.append({
#                     'name': student.name,
#                     'father_name': student.father,  # Use 'father' instead of 'father_name'
#                     'father_number': student.father_nammber,  # Use 'father_nammber' instead of 'father_number'
#                     'image': student.image.url if student.image else None,
#                     'info': student.info,
#                     'absent_days': total_absent_days
#                 })
#             # Prepare the response data
            
#             response_data = {
#                 'Teachers': teacher_serializer.data,
#                 'Students': students_count,
#                 'principal_data': student_serializer.data,
#                 'absent_student_days': attendance_today,
#                 'absent_student_name': list(name_data.values(
#                     'student__name', 'is_present', 'school_class__name',
#                     'teacher__name', 'student__father',
#                     'student__father_nammber', 'student__image', 'student__info'
#                 )),
#                 'attendance_name': students_attendance_data  # Include absent days data
#             }

#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)






# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
            
#             # Fetch data
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             students_count = Student.objects.count()
#             teachers = Teacher.objects.all()
            
#             # Serialize data
#             student_serializer = StudentSerializer(principal_data, many=True)
#             teacher_serializer = TeacherSerializer(teachers, many=True)
            
#             # Calculate days absent for each student
#             students_attendance_data = []
#             for student in principal_data:
#                 total_absent_days = Attendance.objects.filter(student=student, is_present=True).count()
#                 students_attendance_data.append({
#                     'name': student.name,
#                     'father_name': student.father,  # Use 'father' instead of 'father_name'
#                     'father_number': student.father_nammber,  # Use 'father_nammber' instead of 'father_number'
#                     'image': student.image.url if student.image else None,
#                     'info': student.info,
#                     'absent_days': total_absent_days
#                 })
#             # Prepare the response data
#             response_data = {
#                 'Teachers': teacher_serializer.data,
#                 'Students': students_count,
#                 'principal_data': student_serializer.data,
#                 'absent_student_days': attendance_today,
#                 'attendance_name': list(name_data.values(
#                     'student__name', 'is_present', 'school_class__name', 
#                     'teacher__name', 'student__father', 
#                     'student__father_nammber', 'student__image', 'student__info'
#                 )),
#                 'absent_days': students_attendance_data  # Include absent days data
#             }
            
#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
            
#             # Fetch data
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             students_count = Student.objects.count()
#             teachers = Teacher.objects.all()
            
#             # Serialize data
#             student_serializer = StudentSerializer(principal_data, many=True)
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Serialize Teacher objects
            
#             # Prepare the response data
#             response_data = {
#                 'Teachers': teacher_serializer.data,  # Correctly serialize Teacher data
#                 'Students': students_count,
#                 'principal_data': student_serializer.data,
#                 'attendance_today': attendance_today,
#                 'attendance_name': list(name_data.values('student__name', 'is_present', 'school_class__name', 'teacher__name', 'student__father', 'student__father_nammber', 'student__image', 'student__info')),  # Corrected field name
#             }
            
#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)
    
    # today = timezone.now().date()
    
    # # جميع المدرسين الذين لم يسجلوا حضورهم اليوم
    # absent_teachers = Teacher.objects.exclude(
    #     teacherattendance__date=today
    # )
    


from .models import TeacherAttendance

from .models import TeacherAttendance, Teacher
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeacherSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_profiles_data(request):
    if request.user.groups.filter(name='manager').exists():
        if request.method == 'GET':
            today = timezone.now().date()
            
            # Fetch all teacher profiles
            teachers = Teacher.objects.all()
            
            # Serialize Teacher objects
            teacher_serializer = TeacherSerializer(teachers, many=True)

            # Fetch teachers who are present today
            present_teachers = TeacherAttendance.objects.filter(date__date=today, is_present=True).values_list('teacher', flat=True)
            present_teachers_profiles = Teacher.objects.filter(id__in=present_teachers)
            present_teachers_serializer = TeacherSerializer(present_teachers_profiles, many=True)

            # Fetch teachers who are absent today
            absent_teachers_profiles = Teacher.objects.exclude(id__in=present_teachers)
            absent_teachers_serializer = TeacherSerializer(absent_teachers_profiles, many=True)

            # Calculate the number of present and absent teachers
            present_count = present_teachers_profiles.count()
            absent_count = absent_teachers_profiles.count()

            response_data = {
                'Teachers': teacher_serializer.data,
                'teachers_present': present_teachers_serializer.data,  # Profiles of present teachers
                'teachers_absent': absent_teachers_serializer.data,     # Profiles of absent teachers
                'present_count': present_count,  # Number of present teachers
                'absent_count': absent_count     # Number of absent teachers
            }

            return Response(response_data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


from home.models import Student
from home.serializers import StudentSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profiles_data(request):
    if request.user.groups.filter(name='manager').exists():
        if request.method == 'GET':
            today = timezone.now().date()
            
            # Fetch all teacher profiles
            Students = Student.objects.all()
            
            # Serialize Teacher objects
            Students_serializer = StudentSerializer(Students, many=True)

            # Fetch teachers who are present today
            present_teachers = TeacherAttendance.objects.filter(date__date=today, is_present=True).values_list('teacher', flat=True)
            present_teachers_profiles = Teacher.objects.filter(id__in=present_teachers)
            present_teachers_serializer = TeacherSerializer(present_teachers_profiles, many=True)

            # Fetch teachers who are absent today
            absent_teachers_profiles = Teacher.objects.exclude(id__in=present_teachers)
            absent_teachers_serializer = TeacherSerializer(absent_teachers_profiles, many=True)

            # Calculate the number of present and absent teachers
            present_count = present_teachers_profiles.count()
            absent_count = absent_teachers_profiles.count()

            response_data = {
                'Students': Students_serializer.data,
                'teachers_present': present_teachers_serializer.data,  # Profiles of present teachers
                'teachers_absent': absent_teachers_serializer.data,     # Profiles of absent teachers
                'present_count': present_count,  # Number of present teachers
                'absent_count': absent_count     # Number of absent teachers
            }

            return Response(response_data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_student_attendance(request):
    if request.user.groups.filter(name='manager').exists():
        student_id = request.GET.get('student_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not all([start_date, end_date]):
            return Response({"error": "Please provide start_date and end_date"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the dates
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if student_id:  # If searching for a specific student
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

            # Fetch attendance records for the specific student within the date range
            attendance_records = Attendance.objects.filter(
                student=student,
                date__range=[start_date, end_date]
            )

            # Serialize the student data
            student_serializer = StudentSerializer(student)

            # Calculate absence rate
            absence_rate = Attendance.get_absence_rate(student, start_date, end_date)

            # Build response data for a specific student
            response_data = {
                "student": student_serializer.data,
                "attendance_records": list(attendance_records.values('date', 'is_present')),
                "absence_rate": absence_rate,
            }

        else:  # If no student_id is provided, fetch all absent students
            # Fetch all absent students within the date range
            absent_students = Attendance.objects.filter(
                is_present=False,    # Corrected to fetch absent students
                date__range=[start_date, end_date]
            ).values('student').distinct()

            # Fetch student details for absent students
            absent_student_ids = [absent['student'] for absent in absent_students]
            absent_student_details = Student.objects.filter(id__in=absent_student_ids)

            # Serialize the student details
            absent_student_serializer = StudentSerializer(absent_student_details, many=True)

            # Build response data for all absent students
            response_data = {
                "absent_students": absent_student_serializer.data,
                "message": "All absent students retrieved successfully."
            }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def search_student_attendance(request):
#     if request.user.groups.filter(name='manager').exists():
#         student_id = request.GET.get('student_id')
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         if not all([start_date, end_date]):
#             return Response({"error": "Please provide start_date and end_date"}, status=status.HTTP_400_BAD_REQUEST)

#         # Parse the dates
#         start_date = parse_date(start_date)
#         end_date = parse_date(end_date)

#         if student_id:  # If searching for a specific student
#             try:
#                 student = Student.objects.get(id=student_id)
#             except Student.DoesNotExist:
#                 return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#             # Fetch attendance records for the specific student within the date range
#             attendance_records = Attendance.objects.filter(
#                 student=student,
#                 date__range=[start_date, end_date]
#             )

#             # Serialize the student data
#             student_serializer = StudentSerializer(student)

#             # Calculate absence rate
#             absence_rate = Attendance.get_absence_rate(student, start_date, end_date)

#             # Build response data for a specific student
#             response_data = {
#                 "student": student_serializer.data,
#                 "attendance_records": list(attendance_records.values('date', 'is_present')),
#                 "absence_rate": absence_rate,
#             }

#         else:  # If no student_id is provided, fetch all absent students
#             # Fetch all absent students within the date range
#             absent_students = Attendance.objects.filter(
#                 is_present=True,
#                 date__range=[start_date, end_date]
#             ).values('student').distinct()

#             # Fetch attendance records for absent students
#             attendance_records = Attendance.objects.filter(
#                 student__in=absent_students,
#                 date__range=[start_date, end_date]
#             )

#             # Serialize the attendance records
#             attendance_data = list(attendance_records.values('student', 'date', 'is_present'))

#             # Build response data for all absent students
#             response_data = {
#                 "absent_students": attendance_data,
#                 "message": "All absent students retrieved successfully."
#             }

#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def search_student_attendance(request):
#     if request.user.groups.filter(name='manager').exists():
#         student_id = request.GET.get('student_id')
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         if not all([student_id, start_date, end_date]):
#             return Response({"error": "Please provide student_id, start_date, and end_date"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             student = Student.objects.get(id=student_id)
#         except Student.DoesNotExist:
#             return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Parse the dates
#         start_date = parse_date(start_date)
#         end_date = parse_date(end_date)

#         # Fetch attendance records for the student within the date range
#         attendance_records = Attendance.objects.filter(
#             student=student,
#             date__range=[start_date, end_date]
#         )

#         # Serialize the student data
#         student_serializer = StudentSerializer(student)

#         # Calculate absence rate
#         absence_rate = Attendance.get_absence_rate(student, start_date, end_date)

#         # Build response data
#         response_data = {
#             "student": student_serializer.data,
#             "attendance_records": list(attendance_records.values('date', 'is_present')),
#             "absence_rate": absence_rate,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)








from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class GenerateSongView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "")
        if not user_message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
        payload = {
            "messages": [{"role": "user", "content": user_message}],
            "model": "gpt-4o",
            "max_tokens": 100,
            "temperature": 0.9
        }
        headers = {
            "x-rapidapi-key": "f7e52169e8mshc4c1e3dac030bf5p1e816fjsnf21404c79c3e",
            "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        try:
            # إرسال الطلب إلى API
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # تحقق من نجاح الطلب
            
            # استخراج البيانات من الرد
            data = response.json()
            message = data['choices'][0]['message']['content']
            
            # إرسال الرد إلى العميل
            return Response({"response": message}, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def teacher_profiles_data(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
            
#             # Fetch all teacher profiles
#             teachers = Teacher.objects.all()
            
#             # Serialize Teacher objects
#             teacher_serializer = TeacherSerializer(teachers, many=True)

#             # Fetch teachers who are present today
#             present_teachers = TeacherAttendance.objects.filter(date__date=today, is_present=True).values_list('teacher', flat=True)
#             present_teachers_profiles = Teacher.objects.filter(id__in=present_teachers)
#             present_teachers_serializer = TeacherSerializer(present_teachers_profiles, many=True)

#             # Fetch teachers who are absent today
#             absent_teachers_profiles = Teacher.objects.exclude(id__in=present_teachers)
#             absent_teachers_serializer = TeacherSerializer(absent_teachers_profiles, many=True)

#             response_data = {
#                 'Teachers': teacher_serializer.data,
#                 'teachers_present': present_teachers_serializer.data,  # Profiles of present teachers
#                 'teachers_absent': absent_teachers_serializer.data     # Profiles of absent teachers
#             }

#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def teacher_profiles_data(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
#             # Fetch all teacher profiles
#             teachers = Teacher.objects.all()
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Serialize Teacher objects
#             # Fetch teachers who are marked present
#             #الحاضرين
#             present_teachers = TeacherAttendance.objects.filter(date__date=today, is_present=True).count()
#             # Fetch teachers who are absent (i.e., not in today's attendance)
#             #الغابين
#             teachers_absent = Teacher.objects.exclude(teacherattendance__date__date=today).count()
#             response_data = {
#                 'Teachers': teacher_serializer.data,
#                 'teachers_present': present_teachers,
#                 'teachers_absent': teachers_absent
#             }

#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def teacher_profiles_data(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
#             teachers = Teacher.objects.all()
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Serialize Teacher objects
#             teachers_absent = Teacher.objects.exclude(teacherattendance__date__date=today).count()

#             response_data = {
#                 'Teachers': teacher_serializer.data, 
#                 'teachers_absent':teachers_absent
#             }
            
#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)









#يجيب اسماء الطلبة الغايبين والحضور واجمالي عدد الطلبة في المدرسة
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             principal_data = Student.objects.all()
#             today = timezone.now().date()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             Studentes= Student.objects.all().count()
#             Teachers=Teacher.objects.all()
            
#             # Serialize the principal_data
#             serializer = StudentSerializer(principal_data, many=True)
            
#             # Prepare the response data
#             response_data = {
#                 'Teachers':TeacherSerializer.data,
#                 'Studentes':Studentes,
#                 'principal_data': serializer.data,
#                 'attendance_today': attendance_today,
#                 'attendance_name': name_data.values('student__name', 'is_present','school_class__name','teacher__name','student__father','student__father_nammber','student__image','student__info'),  # Customize this as needed
#             }
            
#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)  

#يجيب كل الفصول ويضيف فصل
class SchoolClassListCreateView(generics.ListCreateAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
#حذف واضافة وتعديل الفصل
class SchoolClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")


#


#بيجيب غياب كل الطلبة في الفصول
class DailyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def get(self, request):
        today = timezone.now().date()
        attendance_qs = Attendance.objects.filter(date__date=today).order_by('student', '-date')
        
        # Create a dictionary to store the latest attendance for each student in each class
        latest_attendance = defaultdict(dict)

        for attendance in attendance_qs:
            if attendance.student_id not in latest_attendance[attendance.school_class_id]:
                latest_attendance[attendance.school_class_id][attendance.student_id] = attendance
        
        # Flatten the dictionary into a list of attendance objects
        latest_attendance_list = [
            att for school_class_att in latest_attendance.values() for att in school_class_att.values()
        ]
        
        serializer = AttendanceSerializer(latest_attendance_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#يجيب الفصول
class SchoolClassAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
    def get(self, request, school_class_id):
        school_class = SchoolClass.objects.get(id=school_class_id)
        serializer = SchoolClassSerializer(school_class)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#يجب كل فصل وعدد الطلبة بداخلوا
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
#يجب كل الفصول
class SchoolClass_Test_ListCreateView(generics.ListCreateAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
#يجب كل الطلاب داخل الفصل
class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            school_class = self.kwargs.get('school_class')
            return Student.objects.filter(SchoolClass_data=school_class)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
#يجدب درجات كل طالب

class GradeCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = Grad_serializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # البحث عن الطالب
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student__id=student_id)

        # البحث عن الفصل
        school_class_id = self.request.query_params.get('school_class_id')
        if school_class_id:
            queryset = queryset.filter(school_class__id=school_class_id)

        # البحث عن المدرس
        teacher_id = self.request.query_params.get('teacher_id')
        if teacher_id:
            queryset = queryset.filter(subject__teachers__id=teacher_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save()  # يمكن لأي مستخدم إضافة الدرجات





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BulkGradeSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class BulkGradeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        school_class_id = request.data.get('school_class_id')
        if not school_class_id:
            return Response({"error": "يرجى تحديد الفصل"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            school_class = SchoolClass.objects.get(id=school_class_id)
        except SchoolClass.DoesNotExist:
            return Response({"error": "الفصل غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        subject_id = request.data.get('subject_id')
        if not subject_id:
            return Response({"error": "يرجى تحديد المادة"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "المادة غير موجودة"}, status=status.HTTP_404_NOT_FOUND)

        grades_data = request.data.get('grades', [])
        serializer = BulkGradeSerializer(data=grades_data, many=True)
        if serializer.is_valid():
            for grade_data in serializer.validated_data:
                student_id = grade_data['student_id']
                try:
                    student = Student.objects.get(id=student_id)
                except Student.DoesNotExist:
                    return Response(
                        {"error": f"الطالب بالرقم {student_id} غير موجود"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                Grade.objects.create(
                    student=student,
                    school_class=school_class,
                    subject=subject,
                    grade=grade_data['grade'],
                    final_grade=grade_data['final_grade'],
                    exam_name=grade_data['exam_name'],
                    date=grade_data.get('date', timezone.now()),
                )

            return Response({"message": "تمت إضافة الدرجات بنجاح"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from.serializers import BulkGradeSerializer
# class BulkGradeCreateView(APIView):
#     permission_classes = [IsAuthenticated]


#     def post(self, request, *args, **kwargs):
#         school_class_id = request.data.get('school_class_id')
#         if not school_class_id:
#             return Response({"error": "يرجى تحديد الفصل"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             school_class = SchoolClass.objects.get(id=school_class_id)
#         except SchoolClass.DoesNotExist:
#             return Response({"error": "الفصل غير موجود"}, status=status.HTTP_404_NOT_FOUND)

#         grades_data = request.data.get('grades', [])
#         serializer = BulkGradeSerializer(data=grades_data, many=True)
#         if serializer.is_valid():
#             for grade_data in serializer.validated_data:
#                 student_id = grade_data['student_id']
#                 try:
#                     student = Student.objects.get(id=student_id)
#                 except Student.DoesNotExist:
#                     return Response(
#                         {"error": f"الطالب بالرقم {student_id} غير موجود"},
#                         status=status.HTTP_404_NOT_FOUND,
#                     )

#                 Grade.objects.create(
#                     student=student,
#                     school_class=school_class,
#                     subject=Subject.objects.first(),  # اختر المادة الافتراضية
#                     grade=grade_data['grade'],
#                     final_grade=grade_data['final_grade'],
#                     exam_name=grade_data['exam_name'],
#                     date=grade_data.get('date', timezone.now()),
#                 )

#             return Response({"message": "تمت إضافة الدرجات بنجاح"}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {
#     "school_class_id": 1,
#     "grades": [
#         {
#             "student_id": 101,
#             "grade": 85.5,
#             "final_grade": 100,
#             "exam_name": "امتحان نهاية الفصل"
#         },
#         {
#             "student_id": 102,
#             "grade": 90.0,
#             "final_grade": 100,
#             "exam_name": "امتحان نهاية الفصل"
#         }
#     ]
# }











# class GradeCreateView(generics.ListCreateAPIView):
#     queryset = Grade.objects.all()
#     serializer_class = Grad_serializers
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Get the current user (teacher)
#         teacher = Teacher.objects.get(user=self.request.user)

#         # Filter grades based on user type
#         if self.request.user.groups.filter(name='manager').exists():
#             # If user is a manager, return all grades
#             return super().get_queryset()
#         else:
#             # Filter grades based on the teacher's classes and subjects
#             queryset = Grade.objects.filter(
#                 subject__in=teacher.subjects.all(),
#                 student__schoolclass__in=teacher.classes.all()
#             )

#             # Filter by school class if provided
#             school_class_id = self.request.query_params.get('school_class_id')
#             if school_class_id:
#                 queryset = queryset.filter(student__schoolclass__id=school_class_id)

#             # Filter by teacher (if needed)
#             # Since we are already filtering based on the teacher's subjects, this part may not be necessary.
#             # If you want to ensure you only see grades for a specific teacher, you could add an additional check.
#             # But since the view is already limited to the current teacher's subjects, this might be redundant.

#             return queryset

#     def perform_create(self, serializer):
#         teacher = Teacher.objects.get(user=self.request.user)
#         # Ensure the subject is within the teacher's subjects and student is in the teacher's classes
#         if not serializer.validated_data['subject'] in teacher.subjects.all():
#             raise PermissionDenied("المادة المختارة غير مرتبطة بالمدرس.")
#         if not serializer.validated_data['student'].schoolclass in teacher.classes.all():
#             raise PermissionDenied("الطالب المختار غير مسجل في فصل المدرس.")
#         serializer.save()

# class GradeCreateView(generics.ListCreateAPIView):
#     queryset = Grade.objects.all()
#     serializer_class = Grad_serializers
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.groups.filter(name='manager').exists():
#             return super().get_queryset()  # Return all grades for GET request
#         else:
#             # Filter grades based on the teacher's classes and subjects
#             teacher = Teacher.objects.get(user=self.request.user)
#             return Grade.objects.filter(subject__in=teacher.subjects.all(), student__schoolclass__in=teacher.classes.all())

#     def perform_create(self, serializer):
#         teacher = Teacher.objects.get(user=self.request.user)
#         # Ensure the subject is within the teacher's subjects and student is in the teacher's classes
#         if not serializer.validated_data['subject'] in teacher.subjects.all():
#             raise PermissionDenied("المادة المختارة غير مرتبطة بالمدرس.")
#         if not serializer.validated_data['student'].schoolclass in teacher.classes.all():
#             raise PermissionDenied("الطالب المختار غير مسجل في فصل المدرس.")
#         serializer.save()

# class GradeCreateView(generics.ListCreateAPIView):  # Use ListCreateAPIView to handle both GET and POST
#     queryset = Grade.objects.all()
#     serializer_class = Grad_serializers
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.groups.filter(name='manager').exists():
#             return super().get_queryset()  # Return all grades for GET request
#         else:
#             raise PermissionDenied("You do not have permission to access this resource.")

#     def perform_create(self, serializer):
#         if not self.request.user.groups.filter(name='manager').exists():
#             raise PermissionDenied("You do not have permission to create this resource.")
#         serializer.save()  # Save the new grade instance


#اضافة وعرض المهام
class task_CreateView(generics.ListCreateAPIView):  # Use ListCreateAPIView to handle both GET and POST
    queryset = Task.objects.all()
    serializer_class = Task_serializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()  # Return all grades for GET request
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(name='manager').exists():
            raise PermissionDenied("You do not have permission to create this resource.")
        serializer.save()  # Save the new grade instance


#رساله لي الاباء
class add_masssging_perns_CreateView(generics.ListCreateAPIView):  # Use ListCreateAPIView to handle both GET and POST
    queryset = info_to_Parent.objects.all()
    serializer_class = Task_Parents_serializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()  # Return all grades for GET request
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(name='manager').exists():
            raise PermissionDenied("You do not have permission to create this resource.")
        serializer.save()  # Save the new grade instance

#حذف وتعديل
class add_masssging_perns_int(generics.RetrieveUpdateDestroyAPIView):
    queryset = info_to_Parent.objects.all()
    serializer_class = Task_Parents_serializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")






    # today = timezone.now().date()
    
    # # جميع المدرسين الذين لم يسجلوا حضورهم اليوم
    # absent_teachers = Teacher.objects.exclude(
    #     teacherattendance__date=today
    # )
    



from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from .pdf_utils import generate_attendance_report_pdf  # Assuming you saved your PDF generation code in a file named pdf_utils.py




# c
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report(request):
    report_type = request.query_params.get('report_type', 'daily')
    today = timezone.now().date()

    if report_type == 'daily':
        attendance_data = Attendance.objects.filter(date__date=today).order_by('student__name')
    elif report_type == 'weekly':
        start_week = today - timezone.timedelta(days=today.weekday())
        end_week = start_week + timezone.timedelta(days=6)
        attendance_data = Attendance.objects.filter(date__date__range=[start_week, end_week]).order_by('student__name')
    elif report_type == 'monthly':
        attendance_data = Attendance.objects.filter(date__year=today.year, date__month=today.month).order_by('student__name')
    elif report_type == 'annual':
        attendance_data = Attendance.objects.filter(date__year=today.year).order_by('student__name')
    else:
        return Response({"error": "Invalid report type."}, status=400)

    # Serialize the attendance data if needed
    attendance_data = attendance_data.values('student__name', 'school_class__name', 'date', 'is_present','student__father_nammber','student__father')

    # Generate PDF
    pdf_buffer = generate_attendance_report_pdf(attendance_data, report_type)

    # Return PDF as response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_attendance_report.pdf"'
    return response




from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear  # استيراد الدوال الصحيحة
from .serializers import AttendanceSerializer
from datetime import timedelta

from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear  # استيراد الدوال الصحيحة
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import AttendanceSerializer
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import AttendanceSerializer

from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from rest_framework.response import Response
from rest_framework import generics
from .serializers import AttendanceSerializer




            # today = timezone.now().date()
            
            # # Fetch data
            # principal_data = Student.objects.all()
            # attendance_today = Attendance.objects.filter(date__date=today).count()
            # name_data = Attendance.objects.filter(date__date=today)
            # students_count = Student.objects.count()
            # teachers = Teacher.objects.all()
            





from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from rest_framework.response import Response
from rest_framework import generics
from .serializers import AttendanceSerializer



from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AttendanceSerializer







    # if report_type == 'daily':
    #     attendance_data = Attendance.objects.filter(date__date=today).order_by('student__name')
    # elif report_type == 'weekly':
    #     start_week = today - timezone.timedelta(days=today.weekday())
    #     end_week = start_week + timezone.timedelta(days=6)
    #     attendance_data = Attendance.objects.filter(date__date__range=[start_week, end_week]).order_by('student__name')
    # elif report_type == 'monthly':
    #     attendance_data = Attendance.objects.filter(date__year=today.year, date__month=today.month).order_by('student__name')
    # elif report_type == 'annual':
    #     attendance_data = Attendance.objects.filter(date__year=today.year).order_by('student__name')

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.dateparse import parse_date
from .serializers import AttendanceSerializer
from rest_framework import status

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def attendance_statistics(request, school_class):
    if request.user.groups.filter(name='manager').exists():
        today = timezone.now().date()
        
        # Get start and end dates from request or set default values
        start_date_str = request.query_params.get('start_date', today.replace(month=1, day=1).strftime('%Y-%m-%d'))
        end_date_str = request.query_params.get('end_date', today.strftime('%Y-%m-%d'))

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if start_date > end_date:
            return Response({'error': 'Start date must be before end date.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate absentees for specified date range
        daily_absentees = Attendance.objects.filter(
            school_class=school_class,
            date__date=today,
            is_present=False
        ).count()

        week_absentees = Attendance.objects.filter(
            school_class=school_class,
            date__date__range=[
                today - timezone.timedelta(days=today.weekday()), 
                today - timezone.timedelta(days=today.weekday()) + timezone.timedelta(days=6)
            ],
            is_present=False
        ).count()

        monthly_absentees = Attendance.objects.filter(
            school_class=school_class,
            date__year=today.year,
            date__month=today.month,
            is_present=False
        ).count()

        yearly_absentees = Attendance.objects.filter(
            school_class=school_class,
            date__year=today.year,
            is_present=False
        ).count()

        # Fetch the attendance records
        attendance_records = Attendance.objects.filter(
            school_class=school_class,
            date__range=(start_date, end_date)
        )

        # Serialize the attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Prepare the response data
        response_data = {
            'daily_absentees': daily_absentees,
            'week_absentees': week_absentees,
            'monthly_absentees': monthly_absentees,
            'yearly_absentees': yearly_absentees,
            'attendance_records': serializer.data
        }

        return Response(response_data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def teacher_attendance_statistics(request, teacher_id):
    if request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='teacher').exists():
        today = timezone.now().date()

        # Get start and end dates from request or set default values
        start_date_str = request.query_params.get('start_date', today.replace(month=1, day=1).strftime('%Y-%m-%d'))
        end_date_str = request.query_params.get('end_date', today.strftime('%Y-%m-%d'))

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if start_date > end_date:
            return Response({'error': 'Start date must be before end date.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate absentees for specified date range
        daily_absentees = TeacherAttendance.objects.filter(
            teacher_id=teacher_id,
            date__date=today,
            is_present=True
        ).count()

        week_absentees = TeacherAttendance.objects.filter(
            teacher_id=teacher_id,
            date__date__range=[
                today - timezone.timedelta(days=today.weekday()),
                today - timezone.timedelta(days=today.weekday()) + timezone.timedelta(days=6)
            ],
            is_present=True
        ).count()

        monthly_absentees = TeacherAttendance.objects.filter(
            teacher_id=teacher_id,
            date__year=today.year,
            date__month=today.month,
            is_present=True
        ).count()

        yearly_absentees = TeacherAttendance.objects.filter(
            teacher_id=teacher_id,
            date__year=today.year,
            is_present=True
        ).count()

        # Fetch the attendance records
        attendance_records = TeacherAttendance.objects.filter(
            teacher_id=teacher_id,
            date__range=(start_date, end_date)
        )

        # Serialize the attendance records
        serializer = TeacherAttendanceSerializer(attendance_records, many=True)

        # Prepare the response data
        response_data = {
            'daily_absentees': daily_absentees,
            'week_absentees': week_absentees,
            'monthly_absentees': monthly_absentees,
            'yearly_absentees': yearly_absentees,
            'attendance_records': serializer.data
        }

        return Response(response_data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)




from home.models import Student,Teacher
from.serializers import StudentSerializer
from .serializers import nowTeacherSerializer
class Student_Test_ListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class Teacher_Test_ListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = nowTeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class Subject_ListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = nowTeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import info_to_Parent_by_class, SchoolClass, Student
from .serializers import InfoToParentSerializer

class SendTaskToClassView(CreateAPIView):
    """
    Class-based view for sending tasks to all students in a specific class.
    """
    serializer_class = InfoToParentSerializer

    def post(self, request, class_id, *args, **kwargs):
        try:
            # Get the class by ID
            school_class = SchoolClass.objects.get(id=class_id)
            # Get all students in the class
            students = Student.objects.filter(SchoolClass_data=school_class)
            # Get the task from the request
            task = request.data.get('task')

            if not task:
                return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Create tasks for all students in the class
            for student in students:
                info_to_Parent_by_class.objects.create(
                    student=student,
                    task=task,
                    image=request.data.get('image', None)
                )

            return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)

        except SchoolClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Failed to send tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import  info_to_Parent_by_class
from .serializers import StudentSerializer, InfoToParentSerializer

@api_view(['POST'])
def send_task_to_students(request, class_id):
    try:
        school_class = SchoolClass.objects.get(id=class_id)
        students = Student.objects.filter(SchoolClass_data=school_class)
        task = request.data.get('task')
        
        if not task:
            return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        for student in students:
            # Add logging to check each student being processed
            print(f"Sending task to: {student.name}")
            
            # Try creating the info_to_Parent_by_class object
            try:
                new_entry = info_to_Parent_by_class.objects.create(
                    student=student,
                    task=task,
                    image=request.data.get('image', None)
                )
                print(f"Created task for {student.name}: {new_entry}")
            except Exception as e:
                print(f"Error creating task for {student.name}: {e}")

        return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)
    
    except SchoolClass.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)





from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import info_to_Parent_by_class
from .serializers import InfoToParentSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response


from .models import info_to_Parent_by_class
from .serializers import InfoToParentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import info_to_Parent_by_class, SchoolClass, Student
from .serializers import InfoToParentSerializer

class SendTaskToClassView(CreateAPIView, ListAPIView):
    """
    Class-based view for sending tasks to all students in a specific class and retrieving tasks.
    """
    serializer_class = InfoToParentSerializer

    def get(self, request, class_id, *args, **kwargs):
        try:
            # Get the class by ID
            school_class = SchoolClass.objects.get(id=class_id)
            # Get all students in the class
            students = Student.objects.filter(SchoolClass_data=school_class)
            # Get all tasks related to students in the class
            tasks = info_to_Parent_by_class.objects.filter(student__in=students)

            if not tasks.exists():
                return Response({"message": "No tasks found for this class"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the tasks
            task_serializer = self.get_serializer(tasks, many=True)

            # Prepare the full data context (class and students with their tasks)
            data = {
                "class": {
                    "id": school_class.id,
                    "name": school_class.name,
                    "teacher": school_class.teacher.name if hasattr(school_class, 'teacher') else "N/A",  # Assuming a teacher field
                },
                "students": [
                    {
                        "id": student.id,
                        "name": student.name,
                        # Get tasks for each student
                        "tasks": task_serializer.data
                    } for student in students
                ]
            }

            return Response(data, status=status.HTTP_200_OK)

        except SchoolClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Failed to retrieve tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, class_id, *args, **kwargs):
        try:
            # Get the class by ID
            school_class = SchoolClass.objects.get(id=class_id)
            # Get all students in the class
            students = Student.objects.filter(SchoolClass_data=school_class)
            # Get the task from the request
            task = request.data.get('task')

            if not task:
                return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Create tasks for all students in the class
            for student in students:
                info_to_Parent_by_class.objects.create(
                    student=student,
                    task=task,
                    image=request.data.get('image', None)
                )

            return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)

        except SchoolClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Failed to send tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from.serializers import event_all_Serializer
from.models import event_to_all

class event_to_All_ListCreateView(generics.ListCreateAPIView):
    queryset = event_to_all.objects.all()
    serializer_class = event_all_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

from home.models import Schedule
from.serializers import Class_schedule_Serializer
#جدول الحصص
class Class_schedule_ListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = Class_schedule_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if self.request.user.groups.filter(name='manager').exists():
            queryset = super().get_queryset()
            
            # فلترة باليوم (إذا تم تقديمه كـ query parameter)
            day_of_week = self.request.query_params.get('day_of_week')
            if day_of_week:
                queryset = queryset.filter(day_of_week=day_of_week)
            
            # فلترة بالفصل (إذا تم تقديمه كـ query parameter)
            school_class_id = self.request.query_params.get('school_class')
            if school_class_id:
                queryset = queryset.filter(school_class_id=school_class_id)

            return queryset
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)





# فلترة باليوم:
# إذا كان الـ query parameter day_of_week موجودًا في الطلب (مثل: ?day_of_week=Sunday)، سيتم تصفية الجداول حسب اليوم.
# فلترة بالفصل:
# إذا كان الـ query parameter school_class موجودًا في الطلب (مثل: ?school_class=1)، سيتم تصفية الجداول حسب الفصل المدرسي.
# استخدام الـ API:
# لعرض جداول الحصص ليوم معين وفصل معين:
# GET /schedule/?day_of_week=Sunday&school_class=1
# لتحديد فقط يوم معين:
# GET /schedule/?day_of_week=Sunday
# لتحديد فقط فصل معين:
# GET /schedule/?school_class=1












from.serializers import now_SchoolClassSerializer
class now_SchoolClassDetailView(generics.RetrieveAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = now_SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        






from home.models import Principal
from.serializers import Principal_Serializer
class mangerProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = Principal_Serializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            # Ensure the user is a teacher
            if user.groups.filter(name='manager').exists():
                return Principal.objects.get(user=user)
            else:
                raise PermissionDenied("You do not have permission to access this resource.")
        except Principal.DoesNotExist:
            raise PermissionDenied(" profile not found.")

from django.shortcuts import render
import os
import pandas as pd

def import_students_from_excel(request):
    if request.method == 'POST' and 'file' in request.FILES:
        excel_file = request.FILES['file']
        temp_dir = 'temporary/'  # مسار المجلد المؤقت

        # تأكد من أن المجلد المؤقت موجود، وإن لم يكن موجودًا قم بإنشائه
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # استخدام os.path.join لحفظ الملف في المجلد المؤقت
        file_path = os.path.join(temp_dir, excel_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        added_students = []  # قائمة للطلاب المضافين
        skipped_students = []  # قائمة للطلاب المتجنبين

        try:
            # قراءة ملف Excel باستخدام pandas مع تحديد نوع بعض الأعمدة كنص
            df = pd.read_excel(file_path, dtype={
                'Card ID': str,
                'رقم ولي الأمر': str,
                'رقم الام': str
            })

            # التكرار على كل صف وحفظ البيانات في قاعدة البيانات
            for _, row in df.iterrows():
                # جلب أو إنشاء الفصل إذا لم يكن موجوداً
                school_class, created = SchoolClass.objects.get_or_create(name=row['الفصل'])

                # التحقق مما إذا كان الطالب موجودًا بالفعل بناءً على اسمه
                existing_student = Student.objects.filter(name=row['اسم الطالب']).first()
                if not existing_student:
                    # إنشاء كائن طالب جديد
                    student = Student(
                        name=row['اسم الطالب'],
                        ago=row['العمر'],
                        adres=row['العنوان'],
                        file_namber=row['Card ID'],
                        father=row['اسم ولي الأمر'],
                        father_nammber=row['رقم ولي الأمر'],  # تم ضمان أن الرقم يقرأ كـ string
                        SchoolClass_data=school_class,
                        mother_name=row['اسم الام'],
                        mother_number=row['رقم الام'],
                        gender=row['الجنس']
                    )
                    student.save()

                    # إنشاء المستخدم باستخدام رقم الأم كاسم مستخدم وكلمة مرور باستخدام رقم الأب
                    user = student.user  # الحصول على كائن المستخدم المرتبط بالطالب
                    if not user.username:  # إذا لم يكن اسم المستخدم موجودًا
                        user.username = row['رقم الام']  # استخدام رقم الأم كاسم مستخدم
                        user.set_password(row['رقم ولي الأمر'])  # استخدام رقم الأب ككلمة مرور
                        user.save()

                    # إضافة الطالب إلى قائمة الطلاب المضافين مع اسم المستخدم وكلمة المرور
                    added_students.append({
                        'name': student.name,
                        'username': user.username,
                        'password': user.password,  # يمكنك استخدام كلمة المرور الفعلية هنا إذا كانت متاحة
                    })
                else:
                    # إضافة الطالب إلى قائمة الطلاب المتجنبين
                    skipped_students.append({'name': existing_student.name})

            # حذف الملف المؤقت بعد القراءة
            if os.path.exists(file_path):
                os.remove(file_path)

            # عرض قائمة الطلاب المضافين والمتجنبين
            return render(request, 'import_students.html', {
                'message': 'تم استيراد بيانات الطلاب بنجاح',
                'status': 'success',
                'added_students': added_students,
                'skipped_students': skipped_students,
            })

        except Exception as e:
            return render(request, 'import_students.html', {'message': str(e), 'status': 'error'})

    return render(request, 'import_students.html')




from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
import pandas as pd
from home.models import Student, Attendance, Teacher
import os

def upload_attendance(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        # تحديد نوع الملف بناءً على الامتداد
        file_extension = os.path.splitext(excel_file.name)[1]

        try:
            if file_extension == '.xlsx':
                df = pd.read_excel(excel_file, engine='openpyxl', dtype={'Card ID': str})  # قراءة Card ID كـ str
            elif file_extension == '.xls':
                df = pd.read_excel(excel_file, engine='xlrd', dtype={'Card ID': str})  # قراءة Card ID كـ str
            elif file_extension == '.csv':
                df = pd.read_csv(excel_file, dtype={'Card ID': str})  # قراءة Card ID كـ str
            else:
                raise ValueError("Unsupported file format. Please upload a CSV, .xls, or .xlsx file.")
        except Exception as e:
            messages.error(request, f"Error reading the file: {e}")
            return redirect('upload_attendance')

        # التحقق من وجود الأعمدة المطلوبة
        required_columns = ['Card ID']
        if not all(col in df.columns for col in required_columns):
            messages.error(request, "The file is missing required columns.")
            return redirect('upload_attendance')

        # جلب المعلم الافتراضي
        default_teacher = Teacher.objects.first()
        if not default_teacher:
            messages.error(request, "No default teacher found. Please ensure there is at least one teacher in the database.")
            return redirect('upload_attendance')

        processed_file_numbers = set()
        today = timezone.now().date()

        for index, row in df.iterrows():
            file_number = row['Card ID']
            if file_number in processed_file_numbers:
                continue

            student = Student.objects.filter(file_namber=file_number).first()
            if student:
                school_class = student.SchoolClass_data if student.SchoolClass_data else None
                if school_class:
                    # Check if an attendance record already exists for the student today
                    attendance_record = Attendance.objects.filter(
                        student=student,
                        date__date=today
                    ).first()

                    if attendance_record:
                        # إذا كان السجل موجودًا، يتم فقط تحديث الحضور دون إضافة سجل جديد
                        attendance_record.is_present = True
                        attendance_record.teacher = default_teacher
                        attendance_record.save()
                    else:
                        # إذا لم يكن السجل موجودًا، يتم إنشاء سجل جديد
                        Attendance.objects.create(
                            student=student,
                            school_class=school_class,
                            teacher=default_teacher,
                            date=timezone.now(),
                            is_present=True
                        )

                    processed_file_numbers.add(file_number)
                else:
                    messages.warning(request, f"Student '{file_number}' does not have an associated school class.")
            else:
                messages.warning(request, f"Student with file number '{file_number}' not found in the database.")

        if processed_file_numbers:
            messages.success(request, "Attendance records have been uploaded successfully.")
        else:
            messages.info(request, "No valid attendance records were found to upload.")

        return redirect('upload_attendance')

    return render(request, 'students.html')






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.contrib.auth.models import User



def record_attendance_for_student(student):
    """Helper function to record attendance for a single student."""
    today = now().date()
    if Attendance.objects.filter(student=student, date__date=today).exists():
        return {"message": f"تم تسجيل الحضور مسبقًا للطالب {student.name} اليوم"}

    # تسجيل الحضور
    attendance = Attendance.objects.create(
        school_class=student.SchoolClass_data,
        student=student,
        teacher=Teacher.objects.first(),  # يمكن تعديله إذا كان المعلم جزءًا من الحضور
        is_present=True,
        date=now()
    )

    return {"message": f"تم تسجيل الحضور بنجاح للطالب {student.name}", "attendance_id": attendance.id}

class RecordAttendanceAPIView(APIView):
    def post(self, request):
        if not request.user.groups.filter(name='Gates').exists():
            return Response({"error": "ليس لديك الصلاحية لتنفيذ هذا الإجراء"}, status=status.HTTP_403_FORBIDDEN)

        file_numbers = request.data.get('file_numbers')  # استلام أرقام الملفات من الطلب

        # التحقق من وجود أرقام الملفات
        if not file_numbers:
            return Response({"error": "أرقام الملفات مفقودة"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(file_numbers, list):
            file_numbers = [file_numbers]  # تحويل رقم الملف المفرد إلى قائمة

        results = []
        for file_number in file_numbers:
            try:
                # البحث عن الطالب باستخدام رقم الملف
                student = Student.objects.get(file_namber=file_number)
                result = record_attendance_for_student(student)
            except Student.DoesNotExist:
                result = {"error": f"الطالب برقم الملف {file_number} غير موجود"}  # ضبط النتيجة في حالة الخطأ

            results.append(result)

        return Response(results, status=status.HTTP_200_OK)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils.timezone import now
# from .models import Student, Attendance

# class RecordAttendanceAPIView(APIView):
#     def post(self, request):
#         file_number = request.data.get('file_number')  # استلام رقم الملف من الطلب

#         # التحقق من وجود رقم الملف
#         if not file_number:
#             return Response({"error": "رقم الملف مفقود"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # البحث عن الطالب باستخدام رقم الملف
#             student = Student.objects.get(file_namber=file_number)
#         except Student.DoesNotExist:
#             return Response({"error": "الطالب غير موجود"}, status=status.HTTP_404_NOT_FOUND)

#         # التحقق من تسجيل الحضور لليوم الحالي
#         today = now().date()
#         if Attendance.objects.filter(student=student, date__date=today).exists():
#             return Response({"message": "تم تسجيل الحضور مسبقًا لهذا الطالب اليوم"}, status=status.HTTP_200_OK)

#         # تسجيل الحضور
#         attendance = Attendance.objects.create(
#             school_class=student.SchoolClass_data,
#             student=student,
#             teacher=None,  # يمكن تعديله إذا كان المعلم جزءًا من الحضور
#             is_present=True,
#             date=now()
#         )

#         return Response({"message": "تم تسجيل الحضور بنجاح", "attendance_id": attendance.id}, status=status.HTTP_201_CREATED)














# from django.shortcuts import render, redirect
# from django.utils import timezone
# from django.contrib import messages
# import pandas as pd
# from home.models import Student, Attendance, Teacher
# import os

# def upload_attendance(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']

#         # تحديد نوع الملف بناءً على الامتداد
#         file_extension = os.path.splitext(excel_file.name)[1]

#         try:
#             if file_extension == '.xlsx':
#                 df = pd.read_excel(excel_file, engine='openpyxl')
#             elif file_extension == '.xls':
#                 df = pd.read_excel(excel_file, engine='xlrd')
#             elif file_extension == '.csv':
#                 df = pd.read_csv(excel_file)
#             else:
#                 raise ValueError("Unsupported file format. Please upload a CSV, .xls, or .xlsx file.")
#         except Exception as e:
#             messages.error(request, f"Error reading the file: {e}")
#             return redirect('upload_attendance')

#         # التحقق من وجود الأعمدة المطلوبة
#         required_columns = ['Card ID']
#         if not all(col in df.columns for col in required_columns):
#             messages.error(request, "The file is missing required columns.")
#             return redirect('upload_attendance')

#         # جلب المعلم الافتراضي
#         default_teacher = Teacher.objects.first()
#         if not default_teacher:
#             messages.error(request, "No default teacher found. Please ensure there is at least one teacher in the database.")
#             return redirect('upload_attendance')

#         attendance_records = []
#         processed_file_numbers = set()

#         for index, row in df.iterrows():
#             file_number = row['رقم الملف']
#             if file_number in processed_file_numbers:
#                 continue

#             student = Student.objects.filter(file_namber=file_number).first()
#             if student:
#                 school_class = student.SchoolClass_data if student.SchoolClass_data else None
#                 if school_class:
#                     attendance_records.append(Attendance(
#                         student=student,
#                         school_class=school_class,
#                         teacher=default_teacher,
#                         date=timezone.now(),
#                         is_present=True
#                     ))
#                     processed_file_numbers.add(file_number)
#                 else:
#                     messages.warning(request, f"Student '{file_number}' does not have an associated school class.")
#             else:
#                 messages.warning(request, f"Student with file number '{file_number}' not found in the database.")

#         if attendance_records:
#             Attendance.objects.bulk_create(attendance_records)
#             messages.success(request, "Attendance records have been uploaded successfully.")
#         else:
#             messages.info(request, "No valid attendance records were found to upload.")

#         return redirect('upload_attendance')

#     return render(request, 'students.html')



# from django.shortcuts import render, redirect
# from django.utils import timezone
# import pandas as pd
# from home.models import Student, Attendance

# def upload_attendance(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#         df = pd.read_excel(excel_file)  # قراءة ملف Excel

#         # جلب المعلم الافتراضي (تأكد من وجود معلم افتراضي واحد على الأقل في قاعدة البيانات)
#         default_teacher = Teacher.objects.first()

#         if not default_teacher:
#             print("No default teacher found. Please ensure there is at least one teacher in the database.")
#             return redirect('upload_attendance')

#         attendance_records = []
#         processed_file_numbers = set()  # مجموعة لتتبع أرقام الملفات التي تمت معالجتها

#         for index, row in df.iterrows():
#             file_number = row['رقم الملف']
            
#             # التحقق مما إذا كان الطالب قد تمت معالجته بالفعل
#             if file_number in processed_file_numbers:
#                 continue  # تخطي الطالب إذا كان مكررًا

#             # البحث عن الطالب بناءً على رقم الملف
#             student = Student.objects.filter(file_namber=file_number).first()
            
#             if student:
#                 # استخدام الصف الدراسي الخاص بالطالب إذا كان موجودًا
#                 school_class = student.SchoolClass_data if student.SchoolClass_data else None
#                 if school_class:
#                     attendance_records.append(Attendance(
#                         student=student,
#                         school_class=school_class,
#                         teacher=default_teacher,  # تعيين المعلم الافتراضي
#                         date=timezone.now(),
#                         is_present=True  # تسجيل الحضور
#                     ))
#                     # إضافة رقم الملف إلى المجموعة لمنع التكرار
#                     processed_file_numbers.add(file_number)
#                 else:
#                     print(f"Student '{file_number}' does not have an associated school class.")
#             else:
#                 print(f"Student with file number '{file_number}' not found in the database.")
        
#         # إدخال جميع سجلات الحضور دفعة واحدة
#         Attendance.objects.bulk_create(attendance_records)
        
#         return redirect('upload_attendance')
    
#     return render(request, 'students.html')




# from django.shortcuts import render, redirect
# from django.utils import timezone
# import pandas as pd
# from home.models import Student, Attendance

# def upload_attendance(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#         df = pd.read_excel(excel_file)  # قراءة ملف Excel

#         # جلب المعلم الافتراضي (تأكد من وجود معلم افتراضي واحد على الأقل في قاعدة البيانات)
#         default_teacher = Teacher.objects.first()

#         if not default_teacher:
#             print("No default teacher found. Please ensure there is at least one teacher in the database.")
#             return redirect('upload_attendance')

#         attendance_records = []
#         for index, row in df.iterrows():
#             file_number = row['رقم الملف']
            
#             # البحث عن الطالب بناءً على رقم الملف
#             student = Student.objects.filter(file_namber=file_number).first()
            
#             if student:
#                 # استخدام الصف الدراسي الخاص بالطالب إذا كان موجودًا
#                 school_class = student.SchoolClass_data if student.SchoolClass_data else None
#                 if school_class:
#                     attendance_records.append(Attendance(
#                         student=student,
#                         school_class=school_class,
#                         teacher=default_teacher,  # تعيين المعلم الافتراضي
#                         date=timezone.now(),
#                         is_present=True  # تسجيل الحضور
#                     ))
#                 else:
#                     print(f"Student '{file_number}' does not have an associated school class.")
#             else:
#                 print(f"Student with file number '{file_number}' not found in the database.")
        
#         # إدخال جميع سجلات الحضور دفعة واحدة
#         Attendance.objects.bulk_create(attendance_records)
        
#         return redirect('upload_attendance')
    
#     return render(request, 'students.html')

# from django.shortcuts import render
# import os
# import pandas as pd

# def import_students_from_excel(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#         excel_file = request.FILES['file']
#         temp_dir = 'temporary/'  # مسار المجلد المؤقت

#         # تأكد من أن المجلد المؤقت موجود، وإن لم يكن موجودًا قم بإنشائه
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)

#         # استخدام os.path.join لحفظ الملف في المجلد المؤقت
#         file_path = os.path.join(temp_dir, excel_file.name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in excel_file.chunks():
#                 destination.write(chunk)

#         try:
#             # قراءة ملف Excel باستخدام pandas
#             df = pd.read_excel(file_path)

#             # التكرار على كل صف وحفظ البيانات في قاعدة البيانات
#             for _, row in df.iterrows():
#                 # جلب أو إنشاء الفصل إذا لم يكن موجوداً
#                 school_class, created = SchoolClass.objects.get_or_create(name=row['الفصل'])

#                 # التحقق مما إذا كان الطالب موجودًا بالفعل بناءً على اسمه
#                 if not Student.objects.filter(name=row['اسم الطالب']).exists():
#                     # إنشاء كائن طالب جديد
#                     student = Student(
#                         name=row['اسم الطالب'],
#                         ago=row['العمر'],
#                         adres=row['العنوان'],
#                         file_namber=row['رقم الملف'],
#                         father=row['اسم ولي الأمر'],
#                         father_nammber=str(row['رقم ولي الأمر']),  # تحويل رقم ولي الأمر إلى نص
#                         SchoolClass_data=school_class,
#                         mother_name=row['اسم الام'],
#                         mother_number=row['رقم الام'],
#                         gender=row['الجنس']
#                     )
#                     student.save()

#             # حذف الملف المؤقت بعد القراءة
#             if os.path.exists(file_path):
#                 os.remove(file_path)

#             return render(request, 'import_students.html', {'message': 'تم استيراد بيانات الطلاب بنجاح', 'status': 'success'})

#         except Exception as e:
#             return render(request, 'import_students.html', {'message': str(e), 'status': 'error'})

#     return render(request, 'import_students.html')

# from django.shortcuts import render
# import os
# import pandas as pd

# def import_students_from_excel(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#         excel_file = request.FILES['file']
#         temp_dir = 'temporary/'  # مسار المجلد المؤقت

#         # تأكد من أن المجلد المؤقت موجود، وإن لم يكن موجودًا قم بإنشائه
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)

#         # استخدام os.path.join لحفظ الملف في المجلد المؤقت
#         file_path = os.path.join(temp_dir, excel_file.name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in excel_file.chunks():
#                 destination.write(chunk)

#         try:
#             # قراءة ملف Excel باستخدام pandas
#             df = pd.read_excel(file_path)

#             # التكرار على كل صف وحفظ البيانات في قاعدة البيانات
#             for _, row in df.iterrows():
#                 # جلب أو إنشاء الفصل إذا لم يكن موجوداً
#                 school_class, created = SchoolClass.objects.get_or_create(name=row['الفصل'])

#                 # إنشاء كائن طالب جديد
#                 student = Student(
#                     name=row['اسم الطالب'],
#                     ago=row['العمر'],
#                     adres=row['العنوان'],
#                     file_namber=row['رقم الملف'],
#                     father=row['اسم ولي الأمر'],
#                     father_nammber=str(row['رقم ولي الأمر']),  # تحويل رقم ولي الأمر إلى نص
#                     SchoolClass_data=school_class,
#                     mother_name=row['اسم الام'],
#                     mother_number=row['رقم الام'],
#                     gender=row['الجنس']
#                 )
#                 student.save()

#             # حذف الملف المؤقت بعد القراءة
#             if os.path.exists(file_path):
#                 os.remove(file_path)

#             return render(request, 'import_students.html', {'message': 'تم استيراد بيانات الطلاب بنجاح', 'status': 'success'})

#         except Exception as e:
#             return render(request, 'import_students.html', {'message': str(e), 'status': 'error'})

#     return render(request, 'import_students.html')


# from django.shortcuts import render, redirect
# from django.utils import timezone
# import pandas as pd

# def upload_attendance(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#         df = pd.read_excel(excel_file)  # قراءة ملف Excel
        
#         attendance_records = []
#         for index, row in df.iterrows():
#             student_name = row['رقم الملف']
            
#             # جلب الطالب بناءً على الاسم فقط أو إهمال السطر إذا لم يوجد
#             student = Student.objects.filter(name=student_name).first()
            
#             if student:
#                 # إضافة سجل غياب للطالب
#                 attendance_records.append(Attendance(
#                     student=student,
#                     date=timezone.now(),
#                     is_present=False
#                 ))
#             else:
#                 print(f"Student '{student_name}' not found in the database.")
        
#         # إدخال جميع سجلات الغياب دفعة واحدة
#         Attendance.objects.bulk_create(attendance_records)
        
#         return redirect('upload_attendance')
    
#     return render(request, 'students.html')











# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Student, SchoolClass
# from django.core.files.storage import default_storage
# from .serializers import FileUploadSerializer
# import os
# import pandas as pd

# class ImportStudentsFromExcel(APIView):
#     parser_classes = [MultiPartParser, FormParser]  # لدعم رفع الملفات عبر الطلبات

#     def post(self, request, *args, **kwargs):
#         # تمرير البيانات إلى الـ Serializer
#         file_serializer = FileUploadSerializer(data=request.data)

#         if file_serializer.is_valid():
#             # استلام الملف المرفوع
#             excel_file = request.FILES['file']
#             file_path = default_storage.save(f'temporary/{excel_file.name}', excel_file)

#             try:
#                 # قراءة ملف Excel باستخدام pandas
#                 df = pd.read_excel(file_path)

#                 # التكرار على كل صف وحفظ البيانات في قاعدة البيانات
#                 for _, row in df.iterrows():
#                     # جلب الفصل من قاعدة البيانات إذا كان موجوداً
#                     school_class = SchoolClass.objects.filter(name=row['الفصل']).first()

#                     # إنشاء كائن طالب جديد
#                     student = Student(
#                         name=row['اسم الطالب'],
#                         ago=row['العمر'],
#                         adres=row['العنوان'],
#                         file_namber=row['رقم الملف'],
#                         father=row['اسم ولي الأمر'],
#                         father_nammber=row['رقم ولي الأمر'],
#                         SchoolClass_data=school_class,
#                         mother_name=row['اسم الام'],
#                         mother_number=row['رقم الام'],
#                         gender=row['الجنس']
#                     )
#                     student.save()

#                 # حذف الملف المؤقت بعد القراءة
#                 if os.path.exists(file_path):
#                     os.remove(file_path)

#                 return Response({"status": "success", "message": "تم استيراد بيانات الطلاب بنجاح"}, status=200)

#             except Exception as e:
#                 return Response({"status": "error", "message": str(e)}, status=400)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# import pandas as pd
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# from .models import Student, SchoolClass
# from django.core.files.storage import default_storage
# import os

# class ImportStudentsFromExcel(APIView):
#     parser_classes = [MultiPartParser]  # لدعم رفع الملفات عبر الطلبات

#     def post(self, request, *args, **kwargs):
#         # التأكد من وجود ملف مرفق
#         if 'file' not in request.FILES:
#             return Response({"status": "error", "message": "لم يتم إرسال ملف Excel"}, status=400)
        
#         # استلام الملف المرفوع
#         excel_file = request.FILES['file']
#         file_path = default_storage.save(f'temporary/{excel_file.name}', excel_file)

#         try:
#             # قراءة ملف Excel باستخدام pandas
#             df = pd.read_excel(file_path)

#             # التكرار على كل صف وحفظ البيانات في قاعدة البيانات
#             for _, row in df.iterrows():
#                 # جلب الفصل من قاعدة البيانات إذا كان موجوداً
#                 school_class = SchoolClass.objects.filter(name=row['الفصل']).first()

#                 # إنشاء كائن طالب جديد
#                 student = Student(
#                     name=row['اسم الطالب'],
#                     ago=row['العمر'],
#                     adres=row['العنوان'],
#                     file_namber=row['رقم الملف'],
#                     father=row['اسم ولي الأمر'],
#                     father_nammber=row['رقم ولي الأمر'],
#                     SchoolClass_data=school_class,
#                     mother_name=row['اسم الام'],
#                     mother_number=row['رقم الام'],
#                     gender=row['الجنس']
#                 )
#                 student.save()

#             # حذف الملف المؤقت بعد القراءة
#             if os.path.exists(file_path):
#                 os.remove(file_path)

#             return Response({"status": "success", "message": "تم استيراد بيانات الطلاب بنجاح"}, status=200)

#         except Exception as e:
#             return Response({"status": "error", "message": str(e)}, status=400)











#الجدول حصص
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from .models import Schedule
# from .serializers import ScheduleSerializer
# from django.utils import timezone

# class ScheduleApiView(APIView):
#     def get(self, request):
#         day_of_week = request.query_params.get('day_of_week', timezone.now().strftime('%A'))  # افتراض اليوم الحالي إذا لم يُحدد
#         schedules = Schedule.objects.filter(day_of_week=day_of_week)
#         serializer = ScheduleSerializer(schedules, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ScheduleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SendTaskToClassView(CreateAPIView, ListAPIView):
#     """
#     Class-based view for sending tasks to all students in a specific class and retrieving tasks.
#     """
#     serializer_class = InfoToParentSerializer

#     def get(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get all tasks related to students in the class
#             tasks = info_to_Parent_by_class.objects.filter(student__in=students)

#             if not tasks.exists():
#                 return Response({"message": "No tasks found for this class"}, status=status.HTTP_404_NOT_FOUND)

#             # Serialize the tasks
#             serializer = self.get_serializer(tasks, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to retrieve tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get the task from the request
#             task = request.data.get('task')

#             if not task:
#                 return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # Create tasks for all students in the class
#             for student in students:
#                 info_to_Parent_by_class.objects.create(
#                     student=student,
#                     task=task,
#                     image=request.data.get('image', None)
#                 )

#             return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to send tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class SendTaskToClassView(CreateAPIView):
#     """
#     Class-based view for sending tasks to all students in a specific class.
#     """
#     serializer_class = InfoToParentSerializer

#     def post(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get the task from the request
#             task = request.data.get('task')

#             if not task:
#                 return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # Create tasks for all students in the class
#             for student in students:
#                 info_to_Parent_by_class.objects.create(
#                     student=student,
#                     task=task,
#                     image=request.data.get('image', None)
#                 )

#             return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to send tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class ListTasksByClassView(ListCreateAPIView):
#     """
#     عرض يعتمد على الفئات لعرض جميع المهام للطلاب في فصل معين باستخدام GET،
#     وإنشاء مهام جديدة باستخدام POST، بالإضافة إلى تفاصيل الفصل والطلاب.
#     """
#     serializer_class = InfoToParentSerializer

#     def get(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get all tasks related to students in the class
#             tasks = info_to_Parent_by_class.objects.filter(student__in=students)

#             if not tasks.exists():
#                 return Response({"message": "No tasks found for this class"}, status=status.HTTP_404_NOT_FOUND)

#             # Serialize the tasks
#             task_serializer = self.get_serializer(tasks, many=True)

#             # Prepare the full data context (class and students)
#             data = {
#                 "class": {
#                     "id": school_class.id,
#                     "name": school_class.name,
#                     "teacher": school_class.teacher.name,  # Assuming a teacher field
#                 },
#                 "students": [
#                     {"id": student.id, "name": student.name} for student in students
#                 ],
#                 "tasks": task_serializer.data
#             }

#             return Response(data, status=status.HTTP_200_OK)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to retrieve tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get the data from the request
#             request_data = request.data.copy()
#             # Get the student from the data or handle the case where student is not provided
#             student_id = request_data.get('student')
#             if not student_id:
#                 return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # Check if the student exists and belongs to the provided class
#             student = Student.objects.get(id=student_id, SchoolClass_data=school_class)

#             # Assign the student and class to the task data
#             request_data['student'] = student.id

#             # Serialize the task data
#             serializer = self.get_serializer(data=request_data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Student.DoesNotExist:
#             return Response({"error": "Student not found in this class"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to create task: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# class ListTasksByClassView(ListAPIView):
#     """
#     Class-based view to list all tasks for students in a specific class.
#     """
#     serializer_class = InfoToParentSerializer

#     def get(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get all tasks related to students in the class
#             tasks = info_to_Parent_by_class.objects.filter(student__in=students)

#             if not tasks.exists():
#                 return Response({"message": "No tasks found for this class"}, status=status.HTTP_404_NOT_FOUND)

#             # Serialize the tasks
#             serializer = self.get_serializer(tasks, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to retrieve tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#manger_profile






# @api_view(['GET'])
# def attendance_statistics(request, school_class):
#     if request.user.groups.filter(name='manager').exists():
            
#         today = timezone.now().date()
        
#         # Get start and end dates from request or set default values
#         start_date = request.query_params.get('start_date', today.replace(month=1, day=1))
#         end_date = request.query_params.get('end_date', today)

#         if isinstance(start_date, str):
#             start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
#         if isinstance(end_date, str):
#             end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

#         # Calculate daily absentees
#         attendance_today = Attendance.objects.filter(
#             school_class=school_class,
#             date__date=today,
#             is_present=True
#         ).count()

#         # Calculate weekly absentees
#         start_week = today - timezone.timedelta(days=today.weekday())
#         end_week = start_week + timezone.timedelta(days=6)
#         week_absentees = Attendance.objects.filter(
#             school_class=school_class,
#             date__date__range=[start_week, end_week],
#             is_present=True
#         ).count()

#         # Calculate monthly absentees
#         monthly_absentees = Attendance.objects.filter(
#             school_class=school_class,
#             date__year=today.year,
#             date__month=today.month,
#             is_present=True
#         ).count()

#         # Calculate yearly absentees
#         yearly_absentees = Attendance.objects.filter(
#             school_class=school_class,
#             date__year=today.year,
#             is_present=True
#         ).count()

#         # Fetch the attendance records
#         attendance_records = Attendance.objects.filter(
#             school_class=school_class,
#             date__range=(start_date, end_date)
#         )

#         # Serialize the attendance records
#         serializer = AttendanceSerializer(attendance_records, many=True)

#         # Prepare the response data
#         response_data = {
#             'daily_absentees': attendance_today,
#             'week_absentees': week_absentees,
#             'monthly_absentees': monthly_absentees,
#             'yearly_absentees': yearly_absentees,
#             'attendance_records': serializer.data
#         }

#         return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)





# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def home_api_cont(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             today = timezone.now().date()
            
#             # Fetch data
#             principal_data = Student.objects.all()
#             attendance_today = Attendance.objects.filter(date__date=today).count()
#             name_data = Attendance.objects.filter(date__date=today)
#             students_count = Student.objects.count()
#             teachers = Teacher.objects.all()
            
#             # Serialize data
#             student_serializer = StudentSerializer(principal_data, many=True)
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Serialize Teacher objects
            
#             # Prepare the response data
#             response_data = {
#                 'Teachers': teacher_serializer.data,  # Correctly serialize Teacher data
#                 'Students': students_count,
#                 'principal_data': student_serializer.data,
#                 'attendance_today': attendance_today,
#                 'attendance_name': list(name_data.values('student__name', 'is_present', 'school_class__name', 'teacher__name', 'student__father', 'student__father_nammber', 'student__image', 'student__info')),  # Corrected field name
#             }
            
#             return Response(response_data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)
    










# class AttendanceStatisticsView(generics.ListAPIView):
#     serializer_class = AttendanceSerializer

#     def get_queryset(self):
#         school_class = self.kwargs.get('school_class')
#         start_date = self.request.query_params.get('start_date', timezone.now().replace(month=1, day=1))
#         end_date = self.request.query_params.get('end_date', timezone.now())

#         if isinstance(start_date, str):
#             start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
#         if isinstance(end_date, str):
#             end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')

#         return Attendance.objects.filter(school_class=school_class, date__range=[start_date, end_date])

#     def list(self, request, *args, **kwargs):
#         school_class = self.kwargs.get('school_class')
#         today = timezone.now().date()
        
#         # Get start and end dates from request or set default values
#         start_date = self.request.query_params.get('start_date', timezone.now().replace(month=1, day=1))
#         end_date = self.request.query_params.get('end_date', timezone.now())

#         if isinstance(start_date, str):
#             start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
#         if isinstance(end_date, str):
#             end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')

#         # Calculate daily absentees
#         daily_absentees_count = Attendance.objects.filter(
#             school_class=school_class,
#             date__range=(start_date, end_date),
#             is_present=False
#         ).annotate(day=TruncDay('date')).values('day').annotate(absentee_count=Count('id')).order_by('day')

#         # Calculate monthly absentees
#         monthly_absentees_count = Attendance.objects.filter(
#             school_class=school_class,
#             date__range=(start_date, end_date),
#             is_present=False
#         ).annotate(month=TruncMonth('date')).values('month').annotate(absentee_count=Count('id')).order_by('month')

#         # Calculate yearly absentees
#         yearly_absentees_count = Attendance.objects.filter(
#             school_class=school_class,
#             date__range=(start_date, end_date),
#             is_present=False
#         ).annotate(year=TruncYear('date')).values('year').annotate(absentee_count=Count('id')).order_by('year')

#         # Fetch the attendance records
#         response = super().list(request, *args, **kwargs)
#         response.data = {
#             'daily_absentees': list(daily_absentees_count),
#             'monthly_absentees': list(monthly_absentees_count),
#             'yearly_absentees': list(yearly_absentees_count),
#             'attendance_records': response.data
#         }

#         return Response(response.data)



    # def perform_create(self, serializer):
    #     student = serializer.validated_data.get('student')
    #     if student.SchoolClass_data.representative.user != self.request.user:
    #         raise PermissionDenied("You are not authorized to grade this student.")
    #     serializer.save()


        #    serializer = StudentSerializer(principal_data, many=True)
            
        #     # Prepare the response data
        #     response_data = {
        #         'Studentes':Studentes,
        #         'principal_data': serializer.data,
        #         'attendance_today': attendance_today,
        #         'attendance_name': name_data.values('student__name', 'is_present','school_class__name','teacher__name','student__father','student__father_nammber','student__image','student__info'),  # Customize this as needed
        #     }
            
        #     return Response(response_data)
# class test(generics.ListCreateAPIView):
#     queryset = Principal.objects.all()
#     serializer_class = PrincipalSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # التأكد من أن المستخدم جزء من مجموعة 'manager'
#         if self.request.user.groups.filter(name='manager').exists():
#             return super().get_queryset()
#         else:
#             # رفض الوصول إذا لم يكن المستخدم في المجموعة 'manager'
#             raise PermissionDenied("You do not have permission to access this resource.")

#     def post(self, request, *args, **kwargs):
#         # التأكد من أن المستخدم جزء من مجموعة 'manager'
#         if not self.request.user.groups.filter(name='manager').exists():
#             raise PermissionDenied("You do not have permission to access this resource.")

#         # التحقق من أن الطلب يحتوي على بيانات لإنشاء فصل دراسي
#         if 'class_name' in request.data:
#             # الحصول على اسم الفصل الدراسي من البيانات
#             class_name = request.data.get('class_name')
            
#             # استخدام وظيفة create_class لإنشاء فصل دراسي
#             principal = self.request.user.principal  # أو استخدام Principal.objects.get(user=self.request.user)
#             new_class = principal.create_class(class_name)
            
#             # إرسال استجابة تحتوي على تفاصيل الفصل الدراسي الجديد
#             return Response({
#                 'message': 'Class created successfully',
#                 'class_name': new_class.name
#             }, status=status.HTTP_201_CREATED)
        
#         # إذا لم تكن هناك بيانات لإنشاء الفصل الدراسي، التعامل مع الطلب كإنشاء نموذج Principal
#         return super().post(request, *args, **kwargs)










# #يجيب
# class test(APIView):
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         if self.request.user.groups.filter(name='manager').exists():
#             return super().get_queryset()
#         else:
#             raise PermissionDenied("You do not have permission to access this resource.")
#     def get(self, request):
#         # Retrieve all school classes
#         all_classes = SchoolClass.objects.all()
#         all_classes_serializer = SchoolClassSerializer(all_classes, many=True)

#         # Retrieve classes with absent students
#         absent_classes = SchoolClass.objects.filter(
#             attendance__is_present=False, 
#             attendance__date__date=timezone.now().date()
#         ).distinct()

#         absent_classes_serializer = SchoolClassSerializer(absent_classes, many=True)

#         return Response({
#             'all_classes': all_classes_serializer.data,
#             'absent_classes': absent_classes_serializer.data,
#         }, status=status.HTTP_200_OK)



#تنشئ فصل وتكرت فصل




# class SendTaskToClassView(CreateAPIView):
#     """
#     Class-based view for sending tasks to all students in a specific class.
#     """
#     serializer_class = InfoToParentSerializer

#     def post(self, request, class_id, *args, **kwargs):
#         try:
#             # Get the class by ID
#             school_class = SchoolClass.objects.get(id=class_id)
#             # Get all students in the class
#             students = Student.objects.filter(SchoolClass_data=school_class)
#             # Get the task from the request
#             task = request.data.get('task')

#             if not task:
#                 return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # Create tasks for all students in the class
#             for student in students:
#                 info_to_Parent_by_class.objects.create(
#                     student=student,
#                     task=task,
#                     image=request.data.get('image', None)
#                 )

#             return Response({"message": "Tasks sent successfully"}, status=status.HTTP_201_CREATED)

#         except SchoolClass.DoesNotExist:
#             return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"error": f"Failed to send tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


