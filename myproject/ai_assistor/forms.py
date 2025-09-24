from django import forms

class UploadHomeworkForm(forms.Form):
    homework_image = forms.ImageField(label='上传作业图片')
    student_id = forms.CharField(label='学号', max_length=100)
