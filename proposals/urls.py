from django.urls import path
from .views import (
    ProposalListView, ProposalDetailView, ProposalCreateView,
    ProposalUpdateView, ProposalDeleteView, add_line_item, delete_line_item
)

app_name = 'proposals'

urlpatterns = [
    path('', ProposalListView.as_view(), name='list'),
    path('status/<slug:status_slug>/', ProposalListView.as_view(), name='status'),
    path('create/', ProposalCreateView.as_view(), name='create'),
    path('<slug:slug>/', ProposalDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', ProposalUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', ProposalDeleteView.as_view(), name='delete'),
    path('<slug:slug>/line/add/', add_line_item, name='add_line'),
    path('<slug:slug>/line/<int:line_id>/delete/', delete_line_item, name='delete_line'),
]
