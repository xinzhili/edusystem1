from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    """首页视图"""
    context = {
        'current_page': 'home',
        'user': request.user
    }
    return render(request, 'main/home.html', context)

@login_required
def products_view(request):
    """产品介绍页面视图"""
    products = [
        {'name': '产品A', 'price': '$199', 'stock': '100'},
        {'name': '产品B', 'price': '$99', 'stock': '250'},
        {'name': '产品C', 'price': '$299', 'stock': '50'}
    ]
    context = {
        'current_page': 'products',
        'products': products
    }
    return render(request, 'main/products.html', context)

@login_required
def users_view(request):
    """用户管理页面视图（示例数据）"""
    users = [
        {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
        {'id': 2, 'username': 'user2', 'email': 'user2@example.com'},
        {'id': 3, 'username': 'user3', 'email': 'user3@example.com'}
    ]
    context = {
        'current_page': 'users',
        'users': users
    }
    return render(request, 'main/users.html', context)

@login_required
def settings_view(request):
    """系统设置页面视图"""
    context = {
        'current_page': 'settings',
        'theme_options': ['默认', '蓝色', '绿色', '红色']
    }
    return render(request, 'main/settings.html', context)

@login_required
def about_view(request):
    """关于我们页面视图"""
    context = {
        'current_page': 'about'
    }
    return render(request, 'main/about.html', context)