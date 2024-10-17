import datetime
from django.shortcuts import render
from rest_framework import generics, permissions, pagination, status, response

from notifications.signals import Notify

from .permissions import IsAuthor
from .models import Task, TaskHistory
from .serializers import TaskHistorySerializer, TaskStatusSerializer, TaskSerializer

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    """
    TaskListCreateView to list and create tasks for the authenticated user.

    This view inherits from `generics.ListCreateAPIView` and provides functionality to list all tasks
    for the user making the request and to create new tasks. It uses the `TaskSerializer` to serialize
    the task data and applies the `IsAuthor` and `IsAuthenticated` permission classes to ensure that
    only authenticated users who are the authors of the tasks can access this view.

    Attributes:
        serializer_class (TaskSerializer): The serializer class used to serialize the task data.
        permission_classes (list): The list of permission classes applied to this view.
        pagination_class (pagination.PageNumberPagination): The pagination class used to paginate the task list.
        filterset_fields (dict): The fields that can be used to filter the task list.
        ordering_fields (list): The fields that can be used to order the task list.
        ordering (list): The default ordering applied to the task list.

    Methods:
        get_queryset(self): Returns the queryset of tasks for the authenticated user.
        perform_create(self, serializer: TaskSerializer): Handles the creation of a new task and sends a notification.

    Permissions:
        - IsAuthor: Custom permission to check if the user is the author of the tasks.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filterset_fields = {"Status": ['icontains', 'iexact'], 
                        "PriorityLevel": ['icontains', 'iexact'],
                        "DueDate":['iexact', 'gte', 'lte']}
    ordering_fields = ['-DueDate', 'PriorityLevel']
    ordering = ['DueDate']
    
    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
        
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(author=self.request.user)
        task = Task.objects.get(id=serializer.data.get("id"))
        Notify.send(actor=self.request.user, recipient=self.request.user, verb="Task created", target=task)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    TaskDetailView to retrieve, update, or delete a task for the authenticated user.

    This view inherits from `generics.RetrieveUpdateDestroyAPIView` and provides functionality
    to retrieve, update, or delete a task for the user making the request. It uses the `TaskSerializer`
    to serialize the task data and applies the `IsAuthor` and `IsAuthenticated` permission classes
    to ensure that only authenticated users who are the authors of the tasks can access this view.

    Attributes:
        serializer_class (TaskSerializer): The serializer class used to serialize the task data.
        permission_classes (list): The list of permission classes applied to this view.

    Methods:
        get_queryset(self): Returns the queryset of tasks for the authenticated user.
        perform_update(self, serializer: TaskSerializer): Updates a task if it is not completed and sends a notification.
        perform_destroy(self, instance): Deletes a task and sends a notification.

    Permissions:
        - IsAuthor: Custom permission to check if the user is the author of the task.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer:TaskSerializer):
        #TODO: implement feature to make task unchangeable if completed
        task: Task = self.get_object()
        if task.Status == "Completed":
            return response.Response(data={"detail": "task is completed and cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)
        
        Notify.send(actor=self.request.user, recipient=task.author, verb=f"Task {task.Title} has been updated", target=task)
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        Notify.send(actor=self.request.user, recipient=instance.author, verb=f"Task {instance.Title} has been deleted", target=instance)
        try:
                history = TaskHistory.objects.get(task=instance, author=self.request.user)
                history.delete()
        except TaskHistory.DoesNotExist:
            ## TaskHistory was not found
            pass
        return super().perform_destroy(instance)
    
    
class ToggleTaskStatusView(generics.GenericAPIView):
    """
    ToggleTaskStatusView to toggle the status of a task between "Completed" and "Pending" for the authenticated user.

    This view inherits from `generics.GenericAPIView` and allows the user to toggle the status of a task they own.
    It uses the `TaskStatusSerializer` to serialize the task data and applies the `IsAuthor` and `IsAuthenticated`
    permission classes to ensure that only authenticated users who are the authors of the tasks can access this view.

    Attributes:
        serializer_class (TaskStatusSerializer): The serializer class used to serialize the task data.
        permission_classes (list): The list of permission classes applied to this view.

    Methods:
        get_queryset(self): Returns the queryset of tasks for the authenticated user.
        post(self, request, *args, **kwargs): Toggles the status of the task and sends a notification.

    Permissions:
        - IsAuthor: Custom permission to check if the user is the author of the task.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def post(self, request, *args, **kwargs):
        task: Task = self.get_object()

        if task.Status == "COMPLETED":
            task.Status = "PENDING"
            Notify.send(actor=self.request.user, recipient=task.author, verb=f"Task {task.Title} flagged as pending", target=task)
            try:
                history = TaskHistory.objects.get(task=task, author=request.user)
                history.delete()
            except TaskHistory.DoesNotExist:
                ## TaskHistory was not found
                pass
            
        else:
            task.Status = "COMPLETED"
            Notify.send(actor=self.request.user, recipient=task.author, verb=f"Task {task.Title} is now complete", target=task)
            task.completed_at = datetime.datetime.now(datetime.UTC)
            TaskHistory.objects.create(task=task, author=request.user, completed_at=datetime.datetime.now(datetime.UTC))
        
        task.save()
        return response.Response(data={"detail": "Task status updated"}, status=status.HTTP_200_OK)
    
class TaskHistoryView(generics.ListAPIView):
    """
    TaskHistoryView to list all completed tasks for the authenticated user.

    This view inherits from `generics.ListAPIView` and provides a list of completed tasks
    for the user making the request. It uses the `TaskHistorySerializer` to serialize the
    task history data and applies the `IsAuthor` and `IsAuthenticated` permission classes
    to ensure that only authenticated users who are the authors of the tasks can
    access this view.

    Attributes:
        serializer_class (TaskHistorySerializer): The serializer class used to serialize the task history data.
        permission_classes (list): The list of permission classes applied to this view.
        pagination_class (pagination.PageNumberPagination): The pagination class used to paginate the history data.
        ordering_fields (list): The list of fields that can be used to order the history data.
        ordering (list): The default ordering applied to the history data.

    Methods:
        get_queryset(self): Returns the queryset of task hstory for the authenticated user.

    Permissions:
        - IsAuthor: Custom permission to check if the user is the author of the tasks.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    ordering_fields = ['completed_at']
    ordering = ['-completed_at']

    def get_queryset(self):
        return TaskHistory.objects.filter(author=self.request.user)