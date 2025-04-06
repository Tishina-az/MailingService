from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from config.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser


class UserService:
    """Сервисный класс для работы с пользователями и email-уведомлениями.
    Содержит методы для отправки email-сообщений и обработки верификации пользователей.
    """

    @staticmethod
    def send_verification_email(user_email, host, url):
        """Отправляет email для подтверждения почты пользователя."""

        subject = f'Подтверждение почты на сайте {host}'
        html_message = render_to_string('users/verification_email.html', {
            'host': host,
            'url': url,
        })
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_welcome_email(user_email):
        """Отправляет приветственное письмо новому пользователю."""

        subject = 'Добро пожаловать на наш сайт!'
        html_message = render_to_string('users/welcome_email.html')
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def email_verification(request, token):
        """Обрабатывает верификацию email пользователя по токену."""

        user = get_object_or_404(CustomUser, token=token)
        user.is_active = True
        user.save()

        UserService.send_welcome_email(user.email)
        return redirect(reverse('users:login'))
