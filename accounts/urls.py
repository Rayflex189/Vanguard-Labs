from django.urls import path
from .views import (
    RegisterView, verify_email, CustomLoginView, logout_view,
    profile_view, profile_edit, change_password
)

app_name = 'accounts'

urlpatterns = [
    # Registration & verification
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),

    # Login / Logout
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # Profile
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('password/change/', change_password, name='change_password'),
]
