import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView

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


class CustomUserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    permission_required = 'users.view_customuser'
    paginate_by = 20


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_block = get_object_or_404(CustomUser, pk=pk)

        if user_block == request.user:
            raise PermissionDenied('Вы не можете заблокировать самого себя!')

        if self.request.user.has_perm('users.can_block_user'):
            user_block.is_active=False
            user_block.save()
            return redirect(reverse('users:users_list'))
        else:
            raise PermissionDenied('У вас не достаточно прав для блокировки пользователя.')


class UnBlockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_unblock = get_object_or_404(CustomUser, pk=pk)

        if user_unblock == request.user:
            raise PermissionDenied('Вы не можете заблокировать самого себя!')

        if self.request.user.has_perm('users.can_unblock_user'):
            user_unblock.is_active=True
            user_unblock.save()
            return redirect(reverse('users:users_list'))
        else:
            raise PermissionDenied('У вас не достаточно прав для разблокировки пользователя.')
