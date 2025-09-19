from django.urls import path
from . import views

# 添加这行声明应用命名空间
app_name = 'ai_assistor'

urlpatterns = [
    path('upload/', views.upload_homework, name='upload'),
    path('list/', views.error_list, name='list'),

]