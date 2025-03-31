from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.utils.safestring import mark_safe

from users.models import CustomUser


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'avatar', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Иван'
        })

        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Иванов'
        })

        self.fields['avatar'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">Загрузите изображение в формате JPEG или PNG. Размер не должен превышать 5 МБ.</small>')

    def clean_image(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            valid_formats = ['avatar/jpeg', 'avatar/png']
            if avatar.content_type not in valid_formats:
                raise ValidationError('Формат файла должен быть JPEG или PNG.')

            max_size = 5 * 1024 * 1024
            if avatar.size > max_size:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')
        return avatar


class CustomUserLoginForm(StyleFormMixin, AuthenticationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CustomUserUpdateForm(StyleFormMixin, UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'avatar', 'email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Иван'
        })

        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Иванов'
        })

        self.fields['avatar'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">Загрузите изображение в формате JPEG или PNG. Размер не должен превышать 5 МБ.</small>')

    def clean_image(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            valid_formats = ['avatar/jpeg', 'avatar/png']
            if avatar.content_type not in valid_formats:
                raise ValidationError('Формат файла должен быть JPEG или PNG.')

            max_size = 5 * 1024 * 1024
            if avatar.size > max_size:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')
        return avatar


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })


class CustomSetPasswordForm(StyleFormMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
