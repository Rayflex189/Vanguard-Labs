from django import forms
from contact.models import ContactMessage

class ServiceContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)
        if service:
            self.fields['service_interest'] = forms.CharField(
                initial=service.name,
                widget=forms.HiddenInput()
            )
