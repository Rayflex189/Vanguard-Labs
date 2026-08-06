from django.urls import path
from .views import (
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    ClientContactCreateView, ClientContactUpdateView, ClientContactDeleteView,
    ClientProjectCreateView,
    # Add more as needed
)

app_name = 'clients'

urlpatterns = [
    # Client CRUD
    path('', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('<slug:slug>/', ClientDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', ClientUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', ClientDeleteView.as_view(), name='delete'),

    # Contacts nested under client
    path('<slug:slug>/contact/create/', ClientContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/update/', ClientContactUpdateView.as_view(), name='contact_update'),
    path('contact/<int:pk>/delete/', ClientContactDeleteView.as_view(), name='contact_delete'),

    # Projects nested under client
    path('<slug:slug>/project/create/', ClientProjectCreateView.as_view(), name='project_create'),
    # Add project update/delete if needed
]
