from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mailing.forms import RecipientForm, MessageForm, MailingForm, MailingUpdateForm
from mailing.models import Recipient, Message, Mailing, MailingAttempt
from mailing.services import MailingService, MainPageService


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipient_list'
    context_object_name = 'recipients'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    context_object_name = 'recipient'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not (obj.owner == self.request.user or self.request.user.has_perm('mailing.view_recipient')):
            raise PermissionDenied('У вас не достаточно прав для просмотра данной страницы.')
        return obj


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        obj = self.get_object()

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для редактирования данного клиента.')
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для удаления данного клиента.')
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    context_object_name = 'message'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (obj.owner == self.request.user or self.request.user.has_perm('mailing.view_message')):
            raise PermissionDenied('У вас не достаточно прав для просмотра данной страницы.')
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        obj = self.get_object()

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для редактирования данного сообщения.')
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для удаления данного сообщения.')
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = 'mailings'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (obj.owner == self.request.user or self.request.user.has_perm('mailing.view_mailing')):
            raise PermissionDenied('У вас не достаточно прав для просмотра данной страницы.')
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['recipients'].queryset = Recipient.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingUpdateForm

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        obj = self.get_object()

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для редактирования данной рассылки.')
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для удаления данной рассылки.')
        return obj


class SendMailing(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.owner == self.request.user:
            try:
                count = MailingService.send_mailing(mailing)
                messages.success(request,
                                 f'Рассылка №{pk} успешно отправлена! Получили рассылку: {count} из {mailing.recipients.count()} адресатов.')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке: {str(e)}')
            return redirect(reverse('mailing:mailing_detail', kwargs={'pk': pk}))
        else:
            raise PermissionDenied('У вас не достаточно прав для отправки данной рассылки.')


class MainPageView(TemplateView):
    template_name = 'mailing/main_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = MainPageService.get_mailing_count()
        context['mailing_launched'] = MainPageService.get_mailing_launched()
        context['recipients_count'] = MainPageService.get_recipients_count()
        return context


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'mailing_attempts'
    paginate_by = 20

    # def get_queryset(self):
    #     return MailingAttempt.objects.filter(self.mailing.owner==self.request.user)
