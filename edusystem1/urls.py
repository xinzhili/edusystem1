"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from .views import account_views
from .views import ai_assistor_views

# 为每个应用创建单独的子 URL 配置
account_patterns = ([
    path('login/', account_views.custom_login, name='login'),
    path('register/', account_views.add_student, name='register'), 
], 'account')  # 第二个参数是 namespace

ai_assistor_patterns = ([
    path('upload/', ai_assistor_views.upload_homework, name='upload'),
    path('list/', ai_assistor_views.error_list, name='list'),
], 'ai_assistor')  # 第二个参数是 namespace

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(account_patterns)),  # 包含 account 路由
    path('', include(ai_assistor_patterns)),  # 包含 ai_assistor 路由
    path('', RedirectView.as_view(url='login/')),
]

