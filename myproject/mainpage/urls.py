from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('users/', views.users_view, name='users'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
]