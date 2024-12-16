from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from home.models import Task,Attendance,SchoolClass,Student,Teacher
from .serializers import TaskSerializer,TaskSerializer,Task_updet_Serializer,Attendance_Serializer,SchoolClass_Serializer,Student_Serializer,TeacherSerializer,AcademicTasksSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from.models import Academic_tasks
from manger.serializers import StudentSerializer

class TeacherTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='teacher').exists():
            return Task.objects.filter(assigned_to__user=user)
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

class TeacherTaskUpdateView(generics.UpdateAPIView):
    serializer_class = Task_updet_Serializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='teacher').exists():
            return Task.objects.filter(assigned_to__user=user)
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

    def perform_update(self, serializer):
        user = self.request.user
        if serializer.instance.assigned_to.user == user:
            serializer.save(is_completed=True)
        else:
            raise PermissionDenied("You do not have permission to update this task.")


# عرض الطلاب داخل فصل معين
class SchoolClassListAPIView(generics.ListAPIView):
    serializer_class = SchoolClass_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='teacher').exists():
            return SchoolClass.objects.all()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")

# عرض الطلاب داخل فصل معين
# عرض الطلاب داخل فصل معين
class SchoolClassStudentsAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer  # Use the correct serializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='teacher').exists():
            school_class_id = self.kwargs['pk']
            return Student.objects.filter(SchoolClass_data_id=school_class_id)
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        
from django.utils import timezone
# from datetime import timedelta
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics






from datetime import datetime
class SchoolClassAttendanceToggleAPIView(generics.CreateAPIView):
    serializer_class = Attendance_Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the class ID from the URL
        school_class_id = self.kwargs['pk']

        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract the token from the Authorization header
        try:
            token = auth_header.split(' ')[1]  # Extract the token part
        except IndexError:
            return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate the token and get the teacher
        try:
            token_obj = Token.objects.get(key=token)
            teacher = token_obj.user.teacher
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a mutable copy of request.data
        data = request.data.copy()

        # Assign the class and teacher automatically
        data['school_class'] = school_class_id
        data['teacher'] = teacher.pk

        # Ensure the provided students are valid for the class
        class_students = Student.objects.filter(SchoolClass_data__id=school_class_id)
        student_ids = [student.id for student in class_students]
        toggle_students = data.get('toggle_students', [])

        # Ensure `toggle_students` is a list
        if not isinstance(toggle_students, list):
            return Response({"detail": "'toggle_students' must be a list of student IDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Check that all student IDs in `toggle_students` are valid
        for student_id in toggle_students:
            if int(student_id) not in student_ids:
                return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

        # Get today's date
        today = timezone.now().date()

        # Toggle attendance status for each student in `toggle_students`
        attendance_data = []
        for student_id in toggle_students:
            # Check if the student already has a record for today
            existing_attendance = Attendance.objects.filter(
                student_id=student_id,
                school_class_id=school_class_id,
                teacher=teacher,
                date__date=today  # Match only the date part
            ).first()

            if existing_attendance:
                # If attendance exists, toggle the attendance status (present <-> absent)
                existing_attendance.is_present = not existing_attendance.is_present
                existing_attendance.save()
                attendance_data.append(existing_attendance)
            else:
                # Otherwise, create a new attendance record with time set to midnight
                date_time_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
                attendance_data.append({
                    'school_class': school_class_id,
                    'teacher': teacher.pk,
                    'student': student_id,
                    'is_present': False,  # Initially mark as absent
                    'date': date_time_today
                })

        # Serialize and create Attendance records if new records were created
        new_records = [record for record in attendance_data if isinstance(record, dict)]
        if new_records:
            serializer = self.get_serializer(data=new_records, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        # Return the response with all modified records
        modified_attendance = Attendance.objects.filter(
            student_id__in=toggle_students,
            school_class_id=school_class_id,
            teacher=teacher,
            date__date=today
        )
        response_serializer = Attendance_Serializer(modified_attendance, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)






# from datetime import datetime
# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']

#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Validate the token and get the teacher
#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(SchoolClass_data__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         # Ensure `absent_students` is a list
#         if not isinstance(absent_students, list):
#             return Response({"detail": "'absent_students' must be a list of student IDs."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check that all student IDs in `absent_students` are valid
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Get today's date
#         today = timezone.now().date()

#         # Create Attendance records for each absent student or update if already exists
#         attendance_data = []
#         for student_id in absent_students:
#             # Check if the student already has a record for today
#             existing_attendance = Attendance.objects.filter(
#                 student_id=student_id,
#                 school_class_id=school_class_id,
#                 teacher=teacher,
#                 date__date=today  # Match only the date part
#             ).first()

#             if existing_attendance:
#                 # If attendance exists, toggle the attendance status (present <-> absent)
#                 existing_attendance.is_present = not existing_attendance.is_present
#                 existing_attendance.save()
#                 attendance_data.append(existing_attendance)
#             else:
#                 # Otherwise, create a new attendance record with time set to midnight
#                 date_time_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
#                 attendance_data.append({
#                     'school_class': school_class_id,
#                     'teacher': teacher.pk,
#                     'student': student_id,
#                     'is_present': False,  # Initially mark as absent
#                     'date': date_time_today
#                 })

#         # Serialize and create Attendance records
#         serializer = self.get_serializer(data=attendance_data, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']

#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Validate the token and get the teacher
#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(SchoolClass_data__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         # Ensure `absent_students` is a list
#         if not isinstance(absent_students, list):
#             return Response({"detail": "'absent_students' must be a list of student IDs."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check that all student IDs in `absent_students` are valid
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Get today's date
#         today = timezone.now().date()

#         # List to hold attendance updates
#         attendance_data = []
#         for student_id in absent_students:
#             # Check if the student already has a record for today
#             existing_attendance_today = Attendance.objects.filter(
#                 student_id=student_id,
#                 school_class_id=school_class_id,
#                 teacher=teacher,
#                 date__date=today  # Match only the date part
#             ).first()

#             if existing_attendance_today:
#                 # If attendance exists for today, toggle the attendance status (present <-> absent)
#                 existing_attendance_today.is_present = not existing_attendance_today.is_present
#                 existing_attendance_today.save()

#                 # Add the updated attendance record to the response data
#                 attendance_data.append({
#                     'school_class': school_class_id,
#                     'teacher': teacher.pk,
#                     'student': student_id,
#                     'is_present': existing_attendance_today.is_present,
#                     'date': existing_attendance_today.date
#                 })
#             else:
#                 # Check if the student has any attendance record for any other date
#                 existing_attendance_other_date = Attendance.objects.filter(
#                     student_id=student_id,
#                     school_class_id=school_class_id,
#                     teacher=teacher,
#                 ).first()

#                 if existing_attendance_other_date:
#                     # If attendance exists but not today, add a new record for today
#                     date_time_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
#                     attendance_data.append({
#                         'school_class': school_class_id,
#                         'teacher': teacher.pk,
#                         'student': student_id,
#                         'is_present': False,  # Initially mark as absent
#                         'date': date_time_today
#                     })
#                 else:
#                     # If no attendance exists for the student at all, create a new attendance record
#                     date_time_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
#                     attendance_data.append({
#                         'school_class': school_class_id,
#                         'teacher': teacher.pk,
#                         'student': student_id,
#                         'is_present': False,  # Initially mark as absent
#                         'date': date_time_today
#                     })

#         # If there are no attendance records to update or create
#         if not attendance_data:
#             return Response({"detail": "No attendance records to process."}, status=status.HTTP_400_BAD_REQUEST)

#         # Serialize and return the attendance records (whether new or updated)
#         serializer = self.get_serializer(data=attendance_data, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_200_OK)
# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']

#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Validate the token and get the teacher
#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(SchoolClass_data__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         # Ensure `absent_students` is a list
#         if not isinstance(absent_students, list):
#             return Response({"detail": "'absent_students' must be a list of student IDs."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check that all student IDs in `absent_students` are valid
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Get today's date
#         today = timezone.now().date()

#         # Create Attendance records for each absent student or update if already exists
#         attendance_data = []
#         for student_id in absent_students:
#             # Check if the student already has a record for today
#             existing_attendance = Attendance.objects.filter(
#                 student_id=student_id,
#                 school_class_id=school_class_id,
#                 teacher=teacher,
#                 date__date=today  # Match only the date part
#             ).first()

#             if existing_attendance:
#                 # If attendance exists, toggle the attendance status (present <-> absent)
#                 existing_attendance.is_present = not existing_attendance.is_present
#                 existing_attendance.save()
#                 attendance_data.append(existing_attendance)
#             else:
#                 # Otherwise, create a new attendance record with time set to midnight
#                 date_time_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
#                 attendance_data.append({
#                     'school_class': school_class_id,
#                     'teacher': teacher.pk,
#                     'student': student_id,
#                     'is_present': False,  # Initially mark as absent
#                     'date': date_time_today
#                 })

#         # Serialize and create Attendance records
#         serializer = self.get_serializer(data=attendance_data, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']

#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Validate the token and get the teacher
#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(SchoolClass_data__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         # Ensure `absent_students` is a list
#         if not isinstance(absent_students, list):
#             return Response({"detail": "'absent_students' must be a list of student IDs."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check that all student IDs in `absent_students` are valid
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create Attendance records for each absent student
#         attendance_data = []
#         for student_id in absent_students:
#             attendance_data.append({
#                 'school_class': school_class_id,
#                 'teacher': teacher.pk,
#                 'student': student_id,
#                 'is_present': False,  # Mark as absent
#             })

#         # Serialize and create Attendance records
#         serializer = self.get_serializer(data=attendance_data, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# from rest_framework.response import Response
# from rest_framework import status, generics
# from django.utils import timezone
# from home.models import Attendance, Student, Teacher, SchoolClass
# from manger.serializers import AttendanceSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token

# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = AttendanceSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']

#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(school_classes__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Get attendance records for today
#         today = timezone.now().date()
#         today_attendance = Attendance.objects.filter(
#             school_class__id=school_class_id,
#             date__date=today
#         )

#         # Create attendance summary for today
#         attendance_summary = {
#             "date": today,
#             "total_students": len(student_ids),
#             "present_students": [],
#             "absent_students": [],
#         }

#         for record in today_attendance:
#             if record.is_present:
#                 attendance_summary["present_students"].append({
#                     "id": record.student.id,
#                     "name": record.student.name
#                 })
#             else:
#                 attendance_summary["absent_students"].append({
#                     "id": record.student.id,
#                     "name": record.student.name
#                 })

#         # Process POST request to add absent students (and mark others present)
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         # Update the attendance summary with new data
#         new_attendance = Attendance.objects.filter(
#             school_class__id=school_class_id,
#             date__date=today
#         )

#         for record in new_attendance:
#             if record.is_present and record.student.id not in [s["id"] for s in attendance_summary["present_students"]]:
#                 attendance_summary["present_students"].append({
#                     "id": record.student.id,
#                     "name": record.student.name
#                 })
#             elif not record.is_present and record.student.id not in [s["id"] for s in attendance_summary["absent_students"]]:
#                 attendance_summary["absent_students"].append({
#                     "id": record.student.id,
#                     "name": record.student.name
#                 })

#         return Response({
#             "detail": "Attendance records updated successfully.",
#             "attendance_summary": attendance_summary,
#             "new_record": serializer.data
#         }, status=status.HTTP_201_CREATED)


# class SchoolClassAttendanceCreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']
        
#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()
        
#         # Assign the class and teacher automatically
#         data['school_class'] = school_class_id
#         data['teacher'] = teacher.pk

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(school_classes__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])
        
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)

#         # Process POST request to add absent students
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    


# class SchoolClassAttendance2CreateAPIView(generics.CreateAPIView):
#     serializer_class = Attendance_Serializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Get the class ID from the URL
#         school_class_id = self.kwargs['pk']
        
#         # Get the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return Response({"detail": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Extract the token from the Authorization header
#         try:
#             token = auth_header.split(' ')[1]  # Extract the token part
#         except IndexError:
#             return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             token_obj = Token.objects.get(key=token)
#             teacher = token_obj.user.teacher
#         except Token.DoesNotExist:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
#         except Teacher.DoesNotExist:
#             return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create a mutable copy of request.data
#         data = request.data.copy()

#         # Ensure the provided students are valid for the class
#         class_students = Student.objects.filter(school_classes__id=school_class_id)
#         student_ids = [student.id for student in class_students]
#         absent_students = data.get('absent_students', [])

#         attendance_records = []
#         for student_id in absent_students:
#             if int(student_id) not in student_ids:
#                 return Response({"detail": f"Student with ID {student_id} is not in this class."}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Create attendance record for each student
#             attendance_data = {
#                 'school_class': school_class_id,
#                 'teacher': teacher.pk,
#                 'student': student_id,
#                 'is_present': False
#             }
#             attendance_records.append(attendance_data)

#         # Validate and save all attendance records
#         serializer = self.get_serializer(data=attendance_records, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TeacherProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            # Ensure the user is a teacher
            if user.groups.filter(name='teacher').exists():
                return Teacher.objects.get(user=user)
            else:
                raise PermissionDenied("You do not have permission to access this resource.")
        except Teacher.DoesNotExist:
            raise PermissionDenied("Teacher profile not found.")



def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', True)
    instance = self.get_object()

    # Get the current image
    current_image = instance.image

    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)

    # Restore the image if it was not provided in the update
    if 'image' not in request.data:
        serializer.validated_data['image'] = current_image

    self.perform_update(serializer)

    return Response(serializer.data)



class HomeWorkStudentView(generics.GenericAPIView):
    queryset = Academic_tasks.objects.all()
    serializer_class = AcademicTasksSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='teacher').exists():
            principal_data = self.get_queryset()
            serializer = self.get_serializer(principal_data, many=True)
            teacher = Teacher.objects.get(user=request.user)
            
            school_classes = teacher.classes.all()
            school_class_serializer = SchoolClass_Serializer(school_classes, many=True)

            # Return both the academic tasks and school classes
            return Response({
                'academic_tasks': serializer.data,
                'school_classes': school_class_serializer.data,
            })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='teacher').exists():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)



from manger.models import TeacherAttendance
from manger.serializers import TeacherAttendanceSerializer
#يجب الغياب والحضور   
class TeacherAttendanceListCreateView(generics.ListCreateAPIView):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
            # تحقق من أن المستخدم ينتمي إلى مجموعة "teacher"
            if self.request.user.groups.filter(name='teacher').exists():
                try:
                    teacher = Teacher.objects.get(user=self.request.user)
                except Teacher.DoesNotExist:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # حفظ السجل مع تحديد المدرس الحالي
                serializer.save(teacher=teacher)
            else:
                raise PermissionDenied("You do not have permission to access this resource.")
            


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import leve_student
from .serializers import leve_studentsSerializer

class leave_student(generics.ListCreateAPIView):
  
    serializer_class = leve_studentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='teacher').exists():
            return leve_student.objects.filter(teacher__user=user)
        else:
            raise PermissionDenied("You do not have permission to access this resource.")










# class TeacherAttendance(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
#     date = models.DateTimeField(default=timezone.now)  # Changed to DateTimeField
#     is_present = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ['teacher', 'date']
#         verbose_name = "Teacher Attendance"
#         verbose_name_plural = "Teacher Attendance"

#     def __str__(self):
#         return f'{self.teacher.name} - {self.date}'