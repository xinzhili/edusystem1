from django.shortcuts import render, redirect
from .forms import UploadHomeworkForm
from .models import ErrorRecord
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
import os
import json
from datetime import datetime
from .input_split_analysis import ErrorRecordManager, analyze_document
from django.contrib.auth.decorators import login_required



def upload_homework(request):
    print("Upload homework view called")
    print(f"[DEBUG] upload_view - 用户已登录: {request.user.is_authenticated}")  # 应为True
    # 检查Session中的登录标识（替代is_authenticated）
    if 'user_id' not in request.session:
        return redirect('/accounts/login/')  # 未登录，重定向到登录页
    # 登录成功，获取用户信息并渲染页面
    user_id = request.session['user_id']
    print(f"[DEBUG] upload_view - 用户ID: {request.session.get('user_id')}")  # 应为用户ID
    print(f"{user_id}")
    if request.method == 'POST':
        Myform = UploadHomeworkForm(request.POST, request.FILES)
        if Myform.is_valid():
            # 保存上传的图片
            homework_image = Myform.cleaned_data['homework_image']
            student_id = Myform.cleaned_data['student_id']
            print(f"Received upload for student_id: {student_id}, image name: {homework_image.name}")
            
            # 创建media目录如果不存在
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # 保存图片到media目录
            image_path = os.path.join(settings.MEDIA_ROOT, homework_image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in homework_image.chunks():
                    destination.write(chunk)
            
            # 调用原始代码分析图片
            try:
                # 分析图片并保存错题
                error_data = analyze_document(image_path)
                print("Error data received:", error_data)  # 调试输出
                manager = ErrorRecordManager()
                print("实例化ErrorRecordManager", manager)
                success, saved_records = manager.save_individual_errors(student_id, error_data)
                print("saved records:", saved_records)   
                if success:
                    # 直接渲染列表页，传递刚保存的记录
                    return render(request, 'ai_assistor/list.html', {
                        'errors': saved_records,  # 使用刚保存的记录，不再查询数据库
                        'current_student_id': student_id,
                        'show_new_records': True
                    })
                else:
                    messages.error(request, '错题保存失败')
                    return redirect('ai_assistor:upload')
            
            except Exception as e:
                messages.error(request, f'处理错误: {str(e)}')
                return redirect('ai_assistor:upload')
    else:
        Myform = UploadHomeworkForm()
    
    return render(request, 'ai_assistor/upload.html', {'form': Myform})

@login_required
def error_list(request):
    """保留这个视图用于直接访问/list/时显示所有记录"""
    student_id = request.GET.get('student_id')
    errors = ErrorRecord.objects.all()
    if student_id:
        errors = errors.filter(student_id=student_id)
    
    return render(request, 'ai_assistor/list.html', {
        'errors': errors,
        'current_student_id': student_id,
        'show_new_records': False
    })