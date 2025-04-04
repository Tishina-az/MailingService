from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from config.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser


class UserService:

    @staticmethod
    def send_verification_email(user_email, host, url):
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
        user = get_object_or_404(CustomUser, token=token)
        user.is_active = True
        user.save()

        request.send_welcome_email(user.email)
        return redirect(reverse('users:login'))
