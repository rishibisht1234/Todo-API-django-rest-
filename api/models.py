from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    completed=models.BooleanField(default=False,blank=True,null=True)
    assigned_to=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='assigned_tasks')
    assigned_by=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='created_tasks')
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    completed_at=models.DateTimeField(auto_now=True, blank=True, null=True)
    deadline=models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None  
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
    
    