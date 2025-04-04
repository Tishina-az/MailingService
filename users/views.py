import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm, CustomPasswordResetForm, \
    CustomSetPasswordForm
from users.models import CustomUser
from users.services import UserService


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
        UserService.send_verification_email(user.email, host, url)
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
