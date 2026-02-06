import nh3
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import Contact


class Nh3CleanCharField(forms.CharField):
    def __init__(self,
                 *args,
                 allowed_tags=None,
                 allowed_attributes=None,
                 **kwargs):
        settings_tags = getattr(settings, 'NH3_ALLOWED_TAGS', set())
        tags = allowed_tags if allowed_tags is not None else settings_tags
        if isinstance(tags, str):
            self.allowed_tags = {tags}
        else:
            self.allowed_tags = set(tags)

        settings_attrs = getattr(settings, 'NH3_ALLOWED_ATTRIBUTES', {})
        attrs = allowed_attributes if allowed_attributes is not None else settings_attrs
        if isinstance(attrs, dict):
            self.allowed_attributes = attrs
        else:
            self.allowed_attributes = {}

        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if value:
            value = nh3.clean(
                value,
                tags=self.allowed_tags,
                attributes=self.allowed_attributes,
                link_rel="nofollow noopener noreferrer",
            )
        return value


class ContactForm(forms.ModelForm):
    first_name = Nh3CleanCharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'John',
                'class':
                'w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-uj-orange focus:ring-1 focus:ring-uj-orange outline-none transition-all placeholder-slate-600 text-sm',
                'autocomplete': 'name',
            }),
    )
    last_name = Nh3CleanCharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Doe',
                'class':
                'w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-uj-orange focus:ring-1 focus:ring-uj-orange outline-none transition-all placeholder-slate-600 text-sm',
                'autocomplete': 'name',
            }),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class':
                'w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-uj-orange focus:ring-1 focus:ring-uj-orange outline-none transition-all placeholder-slate-600 text-sm',
                'placeholder': 'john@example.com',
            }),
    )

    message = Nh3CleanCharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'How can we help you?',
                'class':
                'w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-uj-orange focus:ring-1 focus:ring-uj-orange outline-none transition-all placeholder-slate-600 text-sm',
                'rows': 4,
                'maxlength': 500,
            }),
    )

    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            action='contact_form',
            attrs={'class': 'recaptcha-hidden'},
        ),
        required=True,
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message', 'captcha']

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '').strip()
        if not name:
            raise ValidationError("First name cannot be empty.")
        if len(name) < 2:
            raise ValidationError("Min 2 characters required.")
        name = ' '.join(w.capitalize() for w in name.split())
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name', '').strip()
        if not name:
            raise ValidationError("Last name cannot be empty.")
        if len(name) < 2:
            raise ValidationError("Min 2 characters required.")
        name = ' '.join(w.capitalize() for w in name.split())
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Email is required.")
        return email

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if not msg:
            raise ValidationError("Message cannot be empty.", code='blank')
        if len(msg) > 500:
            raise ValidationError("Max 500 characters required.",
                                  code='too_long')
        return msg

    def clean_captcha(self):
        captcha_value = self.cleaned_data.get('captcha')
        if hasattr(captcha_value, 'score') and captcha_value.score < 0.4:
            raise ValidationError(
                "reCAPTCHA verification failed. Are you a robot?")
        return captcha_value
