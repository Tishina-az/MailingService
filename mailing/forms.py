from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.utils.safestring import mark_safe

from mailing.models import Recipient, Message, Mailing


class StyleFormMixin():
    """Миксин для стилизации полей формы.

    Автоматически добавляет CSS-классы к полям формы:
    - `form-control` для стандартных полей
    - `form-check-input` для чекбоксов (BooleanField)
    """

    def __init__(self, *args, **kwargs):
        """Инициализирует миксин и применяет стили к полям формы."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class RecipientForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования получателей рассылки."""
    class Meta:
        model = Recipient
        exclude = ['owner',]

    def __init__(self, *args, **kwargs):
        """Инициализирует форму, устанавливает плейсхолдеры и подсказки."""
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
        """Проверяет уникальность email получателя для текущего пользователя."""
        email = self.cleaned_data.get('email')

        owner = getattr(self.instance, 'owner', None)
        if not owner and hasattr(self, 'request') and self.request:
            owner = self.request.user

        if owner and Recipient.objects.filter(email=email, owner=owner).exclude(pk=self.instance.pk).exists():
            raise ValidationError('У вас уже есть получатель с таким email!')

        return email


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования сообщений рассылки."""
    class Meta:
        model = Message
        exclude = ['owner', ]
        labels = {
            'body': 'Содержание письма'
        }


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания рассылки."""
    class Meta:
        model = Mailing
        fields = ['message', 'recipients']

    def __init__(self, *args, **kwargs):
        """Инициализирует форму, добавляет подсказку для поля получателей."""
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['recipients'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Выберите минимум одного получателя.</small>')


class MailingUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма для обновления рассылки (изменения статуса, получателей и сообщения)."""
    class Meta:
        model = Mailing
        fields = ['status', 'message', 'recipients',]

    def __init__(self, *args, **kwargs):
        """Инициализирует форму, добавляет подсказку для поля получателей."""
        super(MailingUpdateForm, self).__init__(*args, **kwargs)

        self.fields['recipients'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">*Выберите минимум одного получателя.</small>')
