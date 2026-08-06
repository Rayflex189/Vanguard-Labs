from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users (registration) with extra fields."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'company', 'job_title')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class CustomUserChangeForm(UserChangeForm):
    """Form for updating user profile (staff only)."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'bio',
                  'date_of_birth', 'company', 'job_title', 'website', 'github', 'linkedin', 'twitter')

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their own profile."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar', 'bio',
                  'date_of_birth', 'company', 'job_title', 'website', 'github', 'linkedin', 'twitter')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
