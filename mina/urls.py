from django.contrib import admin
from django.urls import path ,include
from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('Management/',include('manger.urls')),
    path('teacher/',include('teacher.urls')),
    path('chat/',include('talks.urls')),
    path('student/',include('student.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),


]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
