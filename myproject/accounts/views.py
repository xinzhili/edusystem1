from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import StudentLoginForm
from .models import Student
from django.urls import reverse
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login



def custom_login(request):
    # 获取 next 参数，默认为你的目标页面（例如首页或仪表盘）
    #next_url = request.GET.get('next', reverse('ai_assistor:upload'))
    next_url_from_get = request.GET.get('next', '') 
    default_redirect = reverse('ai_assistor:upload')
    next_url = next_url_from_get.strip() if next_url_from_get else default_redirect
    

    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
           
            
            # 获取学生对象
            #student = Student.objects.get(student_id=student_id)
            print(f"User: {student_id}")
            print(f"密码: {password}")
            # 手动创建用户会话（简化版）
            
            student = Student.objects.get(student_id=student_id)
            print(f"开始验证")
            try:
                 print(f"开始验证2")
                 #user = User.objects.get(username=student_id, password=password) 
                 print(f"开始验证3")
                 # 手动设置Session（替代login）
                 request.session['user_id'] = student_id
                 messages.success(request, f'欢迎 {student.name}！')
                 redirect_to = request.GET.get('next', next_url)
                 print(f"Debug - redirect_to: {redirect_to}")  # 检查最终跳转目标
                 return redirect(redirect_to)
            except User.DoesNotExist:
                 messages.error(request, "学号或密码错误XX")
                 return render(request, "accounts/login.html")  # 重新渲染登录页面，显示错误信息  
            
            
        else:
            # 表单无效时，添加错误消息
            messages.error(request, '学号或密码不正确，请重试。')
            print("登录失败: 表单验证失败")   
 
    else:
        form = StudentLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form,'next': next_url})



