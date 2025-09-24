from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    #path('profile/', views.profile_view, name='profile'),
    # 可以添加 logout 路径，使用 Django 内置的 logout_view
]