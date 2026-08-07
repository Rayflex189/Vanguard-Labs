from django import forms
from .models import TeamMember

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'email', 'bio', 'skills', 'experience', 'linkedin', 'github', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
