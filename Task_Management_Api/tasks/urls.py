"""
URL configuration for the Task Management API.

This module defines the URL patterns for the task-related views in the application.

Routes:
    - '' : Handles listing and creating tasks via `TaskListCreateView`.
    - '<int:pk>/' : Handles reading, updating, and deleting a specific task via `TaskDetailView`.
    - '<int:pk>/mark/' : Toggles the completion status of a specific task via `ToggleTaskStatusView`.
    - 'history/' : Hnadles listing task history via `TaskHistoryView` 

Views:
    - TaskListCreateView: View for listing and creating tasks.
    - TaskDetailView: View for reading, updating, and deleting a specific task.
    - ToggleTaskStatusView: View for toggling the completion status of a task.
    - TaskHistoryView: View for listing history of completed tasks

"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="list_create_task"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="read_update_delete_task"),
    path("<int:pk>/mark/", views.ToggleTaskStatusView.as_view(), name="toggle_complete_pending_task"),
    path("history/", views.TaskHistoryView.as_view(), name="task_history"),
]
