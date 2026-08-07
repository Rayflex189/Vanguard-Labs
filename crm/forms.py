from django import forms
from .models import Lead, Interaction, Task, Note, Opportunity

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company',
            'job_title', 'website', 'status', 'source', 'score',
            'probability', 'expected_value', 'assigned_to', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['lead', 'client', 'name', 'description', 'service', 'value', 'probability', 'expected_close_date', 'stage', 'assigned_to']
        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'subject', 'details', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'details': forms.Textarea(attrs={'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content', 'is_internal']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
      }
