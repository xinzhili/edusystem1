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
