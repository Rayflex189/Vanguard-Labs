from django.urls import path
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, LeadConvertView,
    TaskListView, TaskCreateView,
    OpportunityCreateView, OpportunityUpdateView,
    InteractionCreateView,
)

app_name = 'crm'

urlpatterns = [
    # Leads
    path('leads/', LeadListView.as_view(), name='lead_list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead_detail'),
    path('leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead_update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),
    path('leads/<int:pk>/convert/', LeadConvertView.as_view(), name='lead_convert'),

    # Tasks
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('leads/<int:lead_id>/task/create/', TaskCreateView.as_view(), name='task_create_for_lead'),

    # Opportunities
    path('opportunities/create/', OpportunityCreateView.as_view(), name='opportunity_create'),
    path('opportunities/<int:pk>/update/', OpportunityUpdateView.as_view(), name='opportunity_update'),

    # Interactions
    path('leads/<int:lead_id>/interaction/create/', InteractionCreateView.as_view(), name='interaction_create'),
]
