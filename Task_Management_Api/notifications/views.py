from django.shortcuts import render
from rest_framework import generics, pagination

from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = pagination.PageNumberPagination
    ordering_fields = ['-timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
class NotificationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)