from django import forms
from .models import NotificationCategory, NotificationPreference

class NotificationPreferenceForm(forms.Form):
    """
    Dynamically build form fields per category.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            categories = NotificationCategory.objects.filter(is_active=True)
            for cat in categories:
                pref, _ = NotificationPreference.objects.get_or_create(user=user, category=cat)
                self.fields[f'email_{cat.slug}'] = forms.BooleanField(
                    required=False,
                    initial=pref.email_enabled,
                    label=f'Email: {cat.name}',
                )
                self.fields[f'push_{cat.slug}'] = forms.BooleanField(
                    required=False,
                    initial=pref.push_enabled,
                    label=f'Push: {cat.name}',
                )
                self.fields[f'in_app_{cat.slug}'] = forms.BooleanField(
                    required=False,
                    initial=pref.in_app_enabled,
                    label=f'In-App: {cat.name}',
                )
