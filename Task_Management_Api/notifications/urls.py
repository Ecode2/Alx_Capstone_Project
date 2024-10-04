from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list_create_notifications"),
    path("<int:pk>/", views.NotificationDetailView.as_view(), name="detail_notification"),
    path("read/", views.ReadNotificationsView.as_view(), name="read_notifications"),
    path("unread/", views.UnreadNotificationsView.as_view(), name="unread_notifications"),
]