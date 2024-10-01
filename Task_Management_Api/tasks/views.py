from django.shortcuts import render
from rest_framework import generics, permissions, pagination, status

from accounts.permissions import IsAuthor

from .models import Task
from .serializers import CompleteTaskSerializer, TaskSerializer

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated] #permissions.AllowAny]
    ordering_fields = ['-DueDate', 'PriorityLevel']
    pagination_class = pagination.PageNumberPagination
    filterset_fields = {"Status": ['icontains', 'iexact'], 
                        "PriorityLevel": ['icontains', 'iexact'],
                        "DueDate":['iexact', 'gte', 'lte']}
    #queryset = Task.objects.all()
    
    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        #TODO: implement feature to make task unchangeable if completed
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
class TaskCompleteView(generics.UpdateAPIView):
    serializer_class = CompleteTaskSerializer
    permission_classes = [IsAuthor, permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        #TODO: change status to completed
        return super().perform_update(serializer)