from django.shortcuts import render
from rest_framework import generics, pagination, response, permissions

from permissions import IsRecipient
from .signals import Notify
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsRecipient, permissions.IsAuthenticated]
    ordering_fields = ['-timestamp', 'read']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
class NotificationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)
    
class ReadNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def get_queryset(self):
        return Notify.get_read_notifications(self.request.user)
    

class UnreadNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def get_queryset(self):
        return Notify.get_unread_notifications(self.request.user)