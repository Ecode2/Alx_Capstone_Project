from django.db import models
from django.contrib.auth.models import User

from categories.models import Category


# Create your models here.
class Task(models.Model):
    """
    Task model representing a task in the task management system.
    Attributes:
        Title (str): The title of the task, with a maximum length of 150 characters.
        Description (str): A detailed description of the task.
        DueDate (datetime): The due date and time for the task.
        PriorityLevel (str): The priority level of the task, which can be 'LOW', 'MEDIUM', or 'HIGH'. Defaults to 'LOW'.
        Status (str): The status of the task, which can be 'PENDING' or 'COMPLETED'. Defaults to 'PENDING'.
        category (Category): The category to which the task belongs. Can be null or blank.
        author (User): The user who created the task.
        completed_at (datetime): The date and time when the task was completed. Can be null.
    Meta:
        ordering (list): Orders the tasks by due date in descending order.
    """
    Title = models.CharField(max_length=150)
    Description = models.TextField()
    DueDate = models.DateTimeField()

    PriorityLevelType = models.TextChoices("PriorityLevelType", "LOW MEDIUM HIGH")
    PriorityLevel = models.CharField(choices=PriorityLevelType.choices, max_length=10, default=PriorityLevelType.LOW)

    StatusType = models.TextChoices("StatusType", "PENDING COMPLETED")
    Status = models.CharField(choices=StatusType.choices, max_length=10, default=StatusType.PENDING)

    category = models.ForeignKey(Category, null=True, blank=True, related_name="tasks", on_delete=models.SET_NULL)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-DueDate']


class TaskHistory(models.Model):
    """
    TaskHistory model representing the history of completed tasks in the task management system.
    Attributes:
        task (Task): A foreign key to the completed task
        author (User): The user who created the task.
        completed_at (datetime): The date and time when the task was completed.
    Meta:
        ordering (list): Orders task history by completion date in descending order.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self) -> str:
        return f"{self.task.Title} - {self.completed_at}"
