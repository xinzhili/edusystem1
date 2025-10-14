from django import forms
from .models import Student 


class UploadHomeworkForm(forms.Form):
    homework_image = forms.ImageField(label='上传作业图片')
    student_id = forms.CharField(label='学号', max_length=100)



class StudentLoginForm(forms.Form):
    student_id = forms.IntegerField(label='学号', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        password = cleaned_data.get('password')
        
        if student_id and password:
            # 手动验证学生凭证
            try:
                student = Student.objects.get(student_id=student_id)
                if student.password != password:  # 注意：这是明文比较
                    raise forms.ValidationError("学号或密码不正确")
                # 将学生对象存储起来，避免重复查询
                cleaned_data['student'] = student
            except Student.DoesNotExist:
                raise forms.ValidationError("学号或密码不正确")
        
        return cleaned_data
    
class StudentForm(forms.ModelForm):
    # 明确指定student_id字段，确保其在表单层面也被处理
    student_id = forms.IntegerField(
        label='学号',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # 为日期字段添加日期选择器
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # 为性别字段添加选择项
    GENDER_CHOICES = [('', '请选择性别'), ('男', '男'), ('女', '女')]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


    
    class Meta:
        model = Student
        fields = '__all__'  # 包含所有模型字段
    
    def clean_student_id(self):
        """验证student_id的唯一性[7,8](@ref)"""
        student_id = self.cleaned_data['student_id']
        
        # 检查是否已存在该student_id（排除当前实例，在编辑时有用）
        if Student.objects.filter(student_id=student_id).exists():
            # 如果是创建新记录，或者是在编辑但student_id已变更
            if not self.instance.pk or self.instance.student_id != student_id:
                raise forms.ValidationError('该学号已存在，请使用唯一的学号。')
        
        return student_id
    
    def clean_password(self):
        """对密码进行基本验证"""
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('密码长度至少为8个字符。')
        return password