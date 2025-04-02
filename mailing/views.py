from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, MailingAttempt
from mailing.services import MailingService, MainPageService


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list'
    context_object_name = 'recipients'
    paginate_by = 10


class RecipientDetailView(DetailView):
    model = Recipient
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    paginate_by = 10


class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    paginate_by = 10


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class SendMailing(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        try:
            count = MailingService.send_mailing(mailing)
            messages.success(request,
                             f'Рассылка №{pk} успешно отправлена! Получили рассылку: {count} из {mailing.recipients.count()} адресатов.')
        except Exception as e:
            messages.error(request, f'Ошибка при отправке: {str(e)}')
        return redirect(reverse('mailing:mailing_detail', kwargs={'pk': pk}))


class MainPageView(TemplateView):
    template_name = 'mailing/main_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = MainPageService.get_mailing_count()
        context['mailing_launched'] = MainPageService.get_mailing_launched()
        context['recipients_count'] = MainPageService.get_recipients_count()
        return context


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'mailing_attempts'
    paginate_by = 20
