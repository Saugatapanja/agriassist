"""
URL configuration for agriassist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from agriassist import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('crop_recommend/', views.crop_recommend,name="crop_recommend"),
    path('crop_recommend/crop_recommend_result/', views.crop_recommend_result,name="crop_recommend_result"),
    path('crop_disease/', views.crop_disease,name="crop_disease"),
    path('crop_disease/crop_disease_result/', views.crop_disease_result,name="crop_disease_result"),
    path('fertilizer_recommend/', views.fertilizer_recommend,name="fertilizer_recommend"),
    path('fertilizer_recommend/fertilizer_recommend_result/', views.fertilizer_recommend_result,name="fertilizer_recommend_result"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)