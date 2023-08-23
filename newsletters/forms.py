from django import forms
from .models import NewsletterEmail


class NewsletterEmailForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )

    class Meta:
        model = NewsletterEmail
        fields = ['email']
