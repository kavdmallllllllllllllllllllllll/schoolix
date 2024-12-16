from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from.serializers import PrincipalSerializer,TaskSerializer,TeacherSerializer
from. models import Principal,Task,Teacher
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def home(request):
    if request.user.groups.filter(name='manager').exists():
        if request.method == 'GET':
            principal_data = Principal.objects.all()
            serializer = PrincipalSerializer(principal_data, many=True)
            return Response(serializer.data)
    
        elif request.method == 'POST':
            serializer = PrincipalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)  
from rest_framework import generics


class ManagerAddTaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            tasks = self.get_queryset()
            teachers = Teacher.objects.all()
            principals = Principal.objects.all()

            # Serialize the tasks, teachers, and principals
            task_serializer = self.get_serializer(tasks, many=True)
            teacher_serializer = TeacherSerializer(teachers, many=True)
            principal_serializer = PrincipalSerializer(principals, many=True)

            return Response({
                'tasks': task_serializer.data,
                'teachers': teacher_serializer.data,
                'principals': principal_serializer.data
            })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def manager_Add_task(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             principal_data = Task.objects.all()
#             serializer = TaskSerializer(principal_data, many=True)
#             return Response(serializer.data)
    
#         elif request.method == 'POST':
#             serializer = TaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN) 
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def manager_Add_task(request):
#     if request.user.groups.filter(name='manager').exists():
#         if request.method == 'GET':
#             tasks = Task.objects.all()
#             teachers = Teacher.objects.all()
#             principals = Principal.objects.all()

#             # Serialize the tasks, teachers, and principals
#             task_serializer = TaskSerializer(tasks, many=True)
#             teacher_serializer = TeacherSerializer(teachers, many=True)  # Assuming you create TeacherSerializer
#             principal_serializer = PrincipalSerializer(principals, many=True)  # Assuming you create PrincipalSerializer

#             return Response({
#                 'tasks': task_serializer.data,
#                 'teachers': teacher_serializer.data,
#                 'principals': principal_serializer.data
#             })
    
#         elif request.method == 'POST':
#             serializer = TaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN)





from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .models import Principal, SchoolClass
from .serializers import PrincipalSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .serializers import PrincipalSerializer

class PrincipalListCreateView(generics.ListCreateAPIView):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if self.request.user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            # رفض الوصول إذا لم يكن المستخدم في المجموعة 'manager'
            raise PermissionDenied("You do not have permission to access this resource.")

    def post(self, request, *args, **kwargs):
        # التأكد من أن المستخدم جزء من مجموعة 'manager'
        if not self.request.user.groups.filter(name='manager').exists():
            raise PermissionDenied("You do not have permission to access this resource.")

        # التحقق من أن الطلب يحتوي على بيانات لإنشاء فصل دراسي
        if 'class_name' in request.data:
            # الحصول على اسم الفصل الدراسي من البيانات
            class_name = request.data.get('class_name')
            
            # استخدام وظيفة create_class لإنشاء فصل دراسي
            principal = self.request.user.principal  # أو استخدام Principal.objects.get(user=self.request.user)
            new_class = principal.create_class(class_name)
            
            # إرسال استجابة تحتوي على تفاصيل الفصل الدراسي الجديد
            return Response({
                'message': 'Class created successfully',
                'class_name': new_class.name
            }, status=status.HTTP_201_CREATED)
        
        # إذا لم تكن هناك بيانات لإنشاء الفصل الدراسي، التعامل مع الطلب كإنشاء نموذج Principal
        return super().post(request, *args, **kwargs)







from rest_framework import generics
from rest_framework.response import Response
from .models import Attendance, SchoolClass
from .serializers import AttendanceSerializer, StudentSerializer

# لعرض جميع الطلاب في فصل معين
class StudentListInClassView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        school_class = SchoolClass.objects.get(id=class_id)
        return school_class.student_set.all()

# لاضافة الحضور
class AttendanceCreateView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer



# class TeacherTaskView(generics.ListAPIView, generics.UpdateAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # عرض المهام المكلف بها المدرس الحالي فقط
#         user = self.request.user
#         if user.groups.filter(name='tescher').exists():
#             return Task.objects.filter(assigned_to__user=user)
#         else:
#             raise PermissionDenied("You do not have permission to access this resource.")

#     def perform_update(self, serializer):
#         # السماح للمدرس فقط بتحديث حالة المهمة إلى مكتملة
#         user = self.request.user
#         if user.groups.filter(name='tescher').exists():
#             # التأكد من أن المستخدم يحدث فقط المهام المكلف بها
#             if serializer.instance.assigned_to.user == user:
#                 serializer.save(is_completed=True)
#             else:
#                 raise PermissionDenied("You do not have permission to update this task.")
#         else:
#             raise PermissionDenied("You do not have permission to update this task.")





        
# class tetcherListCreateView(generics.ListCreateAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # عرض المهام المكلف بها المدرس الحالي فقط
#         user = self.request.user
#         if user.groups.filter(name='tescher').exists():
#             return Task.objects.filter(assigned_to__user=user)
#         else:
#             raise PermissionDenied("You do not have permission to access this resource.")

#     def perform_create(self, serializer):
#         # التأكد من أن المدرس الحالي يقوم بإنشاء مهمة جديدة لنفسه
#         user = self.request.user
#         if user.groups.filter(name='tescher').exists():
#             serializer.save(assigned_to=user.teacher)
#         else:
#             raise PermissionDenied("You do not have permission to create this resource.")
















from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
@api_view(['POST'])
def refresh_token(request):
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # حذف التوكن الحالي (اختياري)
    Token.objects.filter(user=user).delete()

    # إنشاء توكن جديد
    token, created = Token.objects.get_or_create(user=user)

    # إرجاع التوكن الجديد
    return Response({'token': token.key}, status=status.HTTP_200_OK)

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Principal, SchoolClass, Student
# from .serializers import PrincipalSerializer

# class PrincipalListCreateView(generics.ListCreateAPIView):
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

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Principal, SchoolClass, Student
# from .serializers import PrincipalSerializer

# class PrincipalListCreateView(generics.ListCreateAPIView):
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




# @api_view(['POST'])
# def refresh_token(request):
#     user = request.user
#     if user.is_authenticated:
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
# from .models import Principal
# from .serializers import PrincipalSerializer

# class PrincipalListCreateView(generics.ListCreateAPIView):
#     queryset = Principal.objects.all()
#     serializer_class = PrincipalSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # التأكد من أن المستخدم جزء من مجموعة 'manager'
#         if self.request.user.groups.filter(name='manger').exists():
#             return super().get_queryset()
#         else:
#             # رفض الوصول إذا لم يكن المستخدم في المجموعة 'manager'
#             raise PermissionDenied("You do not have permission to access this resource.")

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Principal
# from .serializers import PrincipalSerializer

# class PrincipalListCreateView(generics.ListCreateAPIView):
#     queryset = Principal.objects.all()
#     serializer_class = PrincipalSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # التأكد من أن المستخدم جزء من مجموعة 'manager'
#         if self.request.user.groups.filter(name='manager').exists():
#             return super().get_queryset()
#         else:
#             return Principal.objects.none()  # إرجاع قائمة فارغة إذا لم يكن المستخدم لديه الصلاحيات المطلوبة



# @api_view()
# @permission_classes([IsAuthenticated])
# def manger(request):
#     if request.user.groups.filter(name='manager').exists() :
#         if request.method == 'GET':
#             book_all=book.objects.all()
#             book_serializer=bookSerializer(book_all,many= True)
#             return Response (book_serializer.data,status=status.HTTP_200_OK)
#     else:
#         return Response( status= status.HTTP_400_BAD_REQUEST)

