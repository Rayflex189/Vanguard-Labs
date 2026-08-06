from django import forms
from .models import Client, ClientContact, ClientProject, ClientNote

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['slug', 'created_by', 'created_at', 'updated_at']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = ['full_name', 'job_title', 'email', 'phone', 'mobile', 'is_primary', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class ClientProjectForm(forms.ModelForm):
    class Meta:
        model = ClientProject
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'budget', 'technologies', 'link_to_portfolio']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientNoteForm(forms.ModelForm):
    class Meta:
        model = ClientNote
        fields = ['content', 'is_internal']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
