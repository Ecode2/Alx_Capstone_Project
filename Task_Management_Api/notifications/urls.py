from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications list"),
    path("<int:pk>/", views.NotificationDetailView.as_view(), name="notification detail")
]