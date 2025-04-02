import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm, CustomPasswordResetForm, \
    CustomSetPasswordForm
from users.models import CustomUser


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


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()

    send_welcome_email(user.email)
    return redirect(reverse('users:login'))


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm/{token}/'
        send_verification_email(user.email, host, url)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomUserLoginForm


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'


class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/register.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('mailing:main_page')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
