from django import forms
from .models import Project, Task, Milestone, TimeLog, Comment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'client', 'start_date', 'end_date',
            'estimated_hours', 'status', 'priority', 'budget', 'actual_cost',
            'portfolio_project', 'team_members'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'assigned_to', 'milestone',
            'status', 'priority', 'due_date', 'estimated_hours', 'actual_hours'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'description', 'due_date', 'is_completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['task', 'date', 'hours', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
      }
