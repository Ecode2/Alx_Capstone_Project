from django.urls import path

from . import views

urlpatterns = [
    path("",views.TaskListCreateView.as_view(), name="list_create_task"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="read_update_delete_task"),
    path("<int:pk>/mark/", views.TaskCompleteView.as_view(), name="complete_incomplete_task"),
]