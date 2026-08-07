from django.urls import path
from .views import (
    dashboard,
    ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView,
    TaskCreateView, TaskUpdateView, TaskDeleteView,
)

app_name = 'projects_management'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<slug:slug>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('<slug:project_slug>/task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
