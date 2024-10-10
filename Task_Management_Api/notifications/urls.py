from django.urls import path
"""
URL configuration for the notifications app.

This module defines the URL patterns for the notifications-related views.

Routes:
- '' : Lists and creates notifications using `NotificationListView`.
- '<int:pk>/' : Retrieves, updates, or deletes a specific notification using `NotificationDetailView`.
- 'read/' : Marks notifications as read using `ReadNotificationsView`.
- 'unread/' : Marks notifications as unread using `UnreadNotificationsView`.

Imports:
- path: Function to define URL patterns.
- views: Module containing the view classes for handling notifications.

"""
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list_create_notifications"),
    path("<int:pk>/", views.NotificationDetailView.as_view(), name="detail_notification"),
    path("read/", views.ReadNotificationsView.as_view(), name="read_notifications"),
    path("unread/", views.UnreadNotificationsView.as_view(), name="unread_notifications"),
]