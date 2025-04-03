from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.utils.safestring import mark_safe

from mailing.models import Recipient, Message, Mailing


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['owner',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'например example@example.com'
        })

        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Иван'
        })

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Иванов'
        })

        self.fields['middle_name'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Необязательное поле</small>')

        self.fields['comment'].widget.attrs.update({
            'placeholder': '...начните писать'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        owner = getattr(self.instance, 'owner', None)
        if not owner and hasattr(self, 'request') and self.request:
            owner = self.request.user

        if owner and Recipient.objects.filter(email=email, owner=owner).exclude(pk=self.instance.pk).exists():
            raise ValidationError('У вас уже есть получатель с таким email!')

        return email


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        labels = {
            'body': 'Содержание письма'
        }


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ['started_date', 'ended_date']

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['recipients'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Выберите минимум одного получателя.</small>')
