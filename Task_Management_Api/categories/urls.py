from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.CategoryListCreateView.as_view(), name="list_create_category"),
    path("<int:pk>/", views.CategoryDetailView.as_view(), name="read_update_delete_category")
]