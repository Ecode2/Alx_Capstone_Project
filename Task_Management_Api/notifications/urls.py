from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications_list"),
    path("<int:pk>/", views.NotificationDetailView.as_view(), name="notification_detail"),
    path("read/", views.ReadNotificationsView.as_view(), name="read_notifications"),
    path("read/", views.UnreadNotificationsView.as_view(), name="unread_notifications"),
]