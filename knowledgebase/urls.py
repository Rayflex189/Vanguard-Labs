from django.urls import path
from .views import (
    ArticleListView, ArticleDetailView,
    article_feedback, autocomplete_search
)

app_name = 'knowledgebase'

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', ArticleListView.as_view(), name='category'),
    path('search/', ArticleListView.as_view(), name='search'),
    path('autocomplete/', autocomplete_search, name='autocomplete'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
    path('<slug:slug>/feedback/', article_feedback, name='feedback'),
]
