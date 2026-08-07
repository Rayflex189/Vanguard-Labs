from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage, ContactCategory
import re

class ContactForm(forms.ModelForm):
    """
    Contact form with honeypot and file validation.
    """
    # Honeypot field – hidden from real users, bots will fill it
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'company',
            'subject', 'category', 'service_interest',
            'project_budget', 'timeline', 'message',
            'attachment'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us about your project...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company name (optional)'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject of your message'}),
            'service_interest': forms.TextInput(attrs={'placeholder': 'e.g., Web Development'}),
            'project_budget': forms.TextInput(attrs={'placeholder': 'e.g., $10,000 - $50,000'}),
            'timeline': forms.TextInput(attrs={'placeholder': 'e.g., 3 months'}),
        }

    def clean_honeypot(self):
        """If honeypot is filled, treat as spam."""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise ValidationError("Spam detected.")
        return honeypot

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file:
            # Validate file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("File size must be under 10MB.")
        return file

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic validation: only digits, spaces, +, -, (, )
            if not re.match(r'^[\d\s\+\-\(\)]+$', phone):
                raise ValidationError("Enter a valid phone number.")
        return phone
