from django.shortcuts import render
from rest_framework import generics, pagination, response, permissions, status

from .permissions import IsRecipient
from .signals import Notify
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    """
    NotificationListView is a view that provides a list of notifications for the authenticated user.

    Attributes:
        serializer_class (NotificationSerializer): The serializer class used to serialize the notification data.
        pagination_class (PageNumberPagination): The pagination class used to paginate the notification list.
        permission_classes (list): A list of permission classes that the user must satisfy to access the view.
        ordering_fields (list): A list of fields that can be used to order the notification list.
        ordering (list): The default ordering of the notification list.

    Methods:
        get_queryset(self):
            Returns the queryset of notifications filtered by the authenticated user.

    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = NotificationSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsRecipient, permissions.IsAuthenticated]
    ordering_fields = ['-timestamp', 'read']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
class NotificationDetailView(generics.RetrieveDestroyAPIView):
    """
    NotificationDetailView handles the retrieval and deletion of a single notification.

    Attributes:
        serializer_class (NotificationSerializer): The serializer class used for the view.
        permission_classes (list): List of permission classes that are required to access the view.

    Methods:
        get_queryset(self):
            Returns a queryset of notifications filtered by the current user.
        retrieve(self, request, *args, **kwargs):
            Retrieves a single notification instance. If the notification is unread, it marks it as read before returning the serialized data.

    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.

    """
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
    """
    ReadNotificationsView to list all read notifications for the authenticated user.

    This view inherits from `generics.ListAPIView` and provides a list of read notifications
    for the user making the request. It uses the `NotificationSerializer` to serialize the
    notification data and applies the `IsRecipient` and `IsAuthenticated` permission classes
    to ensure that only authenticated users who are the recipients of the notifications can
    access this view.

    Attributes:
        serializer_class (NotificationSerializer): The serializer class used to serialize the notification data.
        permission_classes (list): The list of permission classes applied to this view.

    Methods:
        get_queryset(self): Returns the queryset of read notifications for the authenticated user.

    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def get_queryset(self):
        return Notify.get_read_notifications(self.request.user)
    

class UnreadNotificationsView(generics.ListAPIView):
    """
    UnreadNotificationsView is a view that provides a list of unread notifications for the authenticated user.

    Attributes:
        serializer_class (NotificationSerializer): The serializer class used to serialize the notification data.
        permission_classes (list): A list of permission classes that the user must pass to access this view.

    Methods:
        get_queryset(self):
            Returns the queryset of unread notifications for the authenticated user.
    
    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def get_queryset(self):
        return Notify.get_unread_notifications(self.request.user)
    
class MarkAllAsReadView(generics.GenericAPIView):
    """
    MarkAllAsReadView to mark all notifications as read for the authenticated user.

    This view requires the user to be authenticated and to have the 'IsRecipient' permission.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access this view.

    Methods:
        post(request, *args, **kwargs): Marks all notifications as read for the authenticated user and returns a success response.

    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.

    Returns:
        Response: A response object with a success message and HTTP status 200.
    """
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Notify.mark_all_as_read(request.user)
        return response.Response(data={"detail": "All notifications marked as read"}, status=status.HTTP_200_OK)

class MarkAllAsUnreadView(generics.GenericAPIView):
    """
    MarkAllAsUnreadView is a view that marks all notifications as unread for the authenticated user.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access this view.

    Methods:
        post(self, request, *args, **kwargs):
            Marks all notifications as unread for the authenticated user and returns a success response.

    Permissions:
        - IsRecipient: Custom permission to check if the user is the recipient of the notifications.
        - IsAuthenticated: Ensures the user is authenticated.
    """
    permission_classes = [IsRecipient, permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Notify.mark_all_as_unread(request.user)
        return response.Response(data={"detail": "All notifications marked as unread"}, status=status.HTTP_200_OK)