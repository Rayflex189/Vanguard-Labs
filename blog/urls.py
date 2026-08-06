from django.urls import path
from .views import BlogListView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('tag/<slug:tag_slug>/', BlogListView.as_view(), name='tag'),
    path('category/<slug:category_slug>/', BlogListView.as_view(), name='category'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='detail'),
]
