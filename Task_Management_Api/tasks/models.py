from django.db import models
from django.contrib.auth.models import User

from categories.models import Category

# Create your models here.
class Task(models.Model):
    Title = models.CharField(max_length=150)
    Description = models.TextField()
    DueDate = models.DateTimeField()

    PriorityLevelType = models.TextChoices("PriorityLevelType", "LOW MEDIUM HIGH")
    PriorityLevel = models.CharField(choices=PriorityLevelType.choices, max_length=10, default=PriorityLevelType.LOW)
    
    StatusType = models.TextChoices("StatusType", "PENDING COMPLETED")
    Status = models.CharField(choices=StatusType.choices, max_length=10, default=StatusType.PENDING)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-DueDate']
