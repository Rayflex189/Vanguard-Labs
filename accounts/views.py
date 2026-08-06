from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import User
from .forms import CustomUserCreationForm, ProfileUpdateForm

# --- Registration with email verification ---
class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        # Send verification email
        self.send_verification_email(user)
        messages.success(self.request, "Registration successful! Please check your email to verify your account.")
        return response

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        user.email_verification_token = token
        user.save(update_fields=['email_verification_token'])
        subject = "Verify your email - Vanguard Labs"
        context = {
            'user': user,
            'uid': uid,
            'token': token,
            'site_name': 'Vanguard Labs',
            'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
            'domain': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000',
        }
        message = render_to_string('accounts/email_verification.html', context)
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.email_verification_token = ''
        user.save(update_fields=['is_email_verified', 'email_verification_token'])
        messages.success(request, "Your email has been verified! You can now log in.")
        return redirect('accounts:login')
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect('accounts:register')

# --- Login (extended) ---
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_email_verified:
            messages.warning(self.request, "Please verify your email before logging in.")
            return redirect('accounts:login')
        return super().form_valid(form)

# --- Logout ---
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')

# --- Profile views ---
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
