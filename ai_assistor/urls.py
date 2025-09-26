from django.urls import path
from ai_assistor.views import account_views
from ai_assistor.views import ai_assistor_views
# 添加这行声明应用命名空间
app_name = 'ai_assistor'

urlpatterns = [
    path('login/', account_views.custom_login, name='login'),
    path('upload/', ai_assistor_views.upload_homework, name='upload'),
    path('list/', ai_assistor_views.error_list, name='list'),

]