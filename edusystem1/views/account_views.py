from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from ..forms import StudentLoginForm , StudentForm
from ..models import Student
from django.urls import reverse
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from django.utils import timezone


def custom_login(request):
    # 获取 next 参数，默认为你的目标页面（例如首页或仪表盘）
    #next_url = request.GET.get('next', reverse('ai_assistor:upload'))
    #next_url_from_get = request.GET.get('next', '') 
    #default_redirect = reverse('ai_assistor/upload.html')
    #next_url = next_url_from_get.strip() if next_url_from_get else default_redirect
    

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
                 #user = User.objects.get(username=student_id, password=password) 
                 # 手动设置Session（替代login）
                 request.session['user_id'] = student_id
                 messages.success(request, f'欢迎 {student.name}！')
                 #redirect_to = request.GET.get('next', next_url)
                 redirect_to = ('ai_assistor:upload')
                 print(f"Debug - redirect_to: {redirect_to}")  # 检查最终跳转目标
                 return redirect(redirect_to)
            except User.DoesNotExist:
                 messages.error(request, "学号或密码错误XX")
                 return render(request, "login.html")  # 重新渲染登录页面，显示错误信息  
            
            
        else:
            # 表单无效时，添加错误消息
            messages.error(request, '学号或密码不正确，请重试。')
            print("登录失败: 表单验证失败")   
 
    else:
        form = StudentLoginForm()
    
    return render(request, 'login.html', {'form': form,})


def add_student(request):
    """添加新学生的视图[3,4](@ref)"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                
                # 手动处理数据保存，确保student_id唯一性
                student = form.save(commit=False)
                print(student.student_id)  # 调试查看值
                print(student.name)  # 调试查看值
                student.created_at = timezone.now()
                # 由于student_id是AutoField，通常不需要手动设置
                # 但这里我们确保表单验证通过
                student.save()
                
                messages.success(request, f'学号{student.student_id}号学生{student.name} 的信息已成功保存！请牢记学号！')
            #   return redirect('student_list')  # 重定向到学生列表页
                redirect_to = ('account:login')
                print(f"Debug - redirect_to: {redirect_to}")  # 检查最终跳转目标
                return redirect(redirect_to)
   
            except Exception as e:
                messages.error(request, f'保存失败：{str(e)}')
        else:
            messages.error(request, '表单数据无效，请检查以下错误。')
    else:
        form = StudentForm()
    
    return render(request, 'register.html', {'form': form})


