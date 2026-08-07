from django import forms
from .models import ArticleFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ArticleFeedback
        fields = ['helpful', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional comments...'}),
            'helpful': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Search')
