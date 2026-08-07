from django import forms
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

class ConversationCreateForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text="Select other participants (you will be included automatically)"
    )
    is_group = forms.BooleanField(required=False, initial=False, label="Group conversation")
    subject = forms.CharField(max_length=200, required=False, label="Subject (optional)")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['participants'].queryset = User.objects.exclude(id=self.user.id)
