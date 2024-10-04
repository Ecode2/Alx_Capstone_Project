import datetime
from django.shortcuts import render
from rest_framework import generics, permissions, pagination, status, response

from notifications.signals import Notify

from .permissions import IsAuthor
from .models import Task
from .serializers import TaskStatusSerializer, TaskSerializer

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
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
        Notify.send(actor=self.request.user, recipient=self.request.user, verb="Task created", target=serializer.validated_data)
        return serializer.save(author=self.request.user)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
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
        return super().perform_destroy(instance)
    
    
class ToggleTaskStatusView(generics.GenericAPIView):
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def post(self, request, *args, **kwargs):
        task: Task = self.get_object()
        if task.Status == "Completed":
            task.Status = "Pending"
            Notify.send(actor=self.request.user, recipient=task.author, verb=f"Task {task.Title} flagged as pending", target=task)
        else:
            task.Status = "Completed"
            Notify.send(actor=self.request.user, recipient=task.author, verb=f"Task {task.Title} is now complete", target=task)
            task.completed_at = datetime.datetime.now(datetime.UTC)
        
        task.save()
        return response.Response(data={"detail": "Task status updated"}, status=status.HTTP_200_OK)
    
class TaskHistoryView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    ordering_fields = ['completed_at', 'DueDate']
    ordering = ['-completed_at']

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user, Status="Completed")
    
class TaskPendingView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    ordering_fields = ['DueDate', 'PriorityLevel']
    ordering = ['DueDate']

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user, Status="Pending")