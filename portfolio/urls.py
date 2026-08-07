from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, autocomplete_projects

app_name = 'portfolio'

urlpatterns = [
    path('', PortfolioListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', PortfolioListView.as_view(), name='category'),
    path('search/', PortfolioListView.as_view(), name='search'),
    path('autocomplete/', autocomplete_projects, name='autocomplete'),
    path('<slug:slug>/', PortfolioDetailView.as_view(), name='detail'),
]
