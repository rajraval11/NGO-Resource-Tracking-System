from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('index')),  # ✅ FIX
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
]
