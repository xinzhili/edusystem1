from django.db import models
# from django.contrib.postgres.fields import JSONField

class ErrorRecord(models.Model):
    student_id = models.CharField(max_length=100)
    original_input_id = models.CharField(max_length=100)
    details = models.JSONField()  # 改为 models.JSONField()
    details_embedding = models.JSONField()  # 改为 models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Error {self.id} for student {self.student_id}"
# Create your models here.

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    grade = models.SmallIntegerField()
    date_of_birth = models.DateField()
    gender = models.TextField()
    region = models.CharField(max_length=20)
    textbook_version = models.CharField(max_length=20)
    school = models.CharField(max_length=30)
    created_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        return f"{self.student_id} - {self.name}"