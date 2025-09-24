from django import forms
from .models import Student

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