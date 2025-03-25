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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
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
        fields = '__all__'
        # Виджет для удобного ввода даты и времени в форме (с помощью календарика)
        widgets = {
            'started_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ended_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        # Проверка существования формы self.instance.pk. Если форма существует,
        # то дата и время отформатируются для корректного отображения в форме (чтобы не вводить их заново)
        if self.instance.pk:
            self.initial['started_date'] = self.instance.started_date.strftime('%Y-%m-%dT%H:%M')
            self.initial['ended_date'] = self.instance.ended_date.strftime('%Y-%m-%dT%H:%M')

        self.fields['started_date'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Введите дату и время в формате: ГГГГ-ММ-ДД, ЧЧ:ММ</small>')

        self.fields['ended_date'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Введите дату и время в формате: ГГГГ-ММ-ДД, ЧЧ:ММ</small>')

        self.fields['recipients'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Выберите минимум одного получателя.</small>')
