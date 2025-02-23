from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.models import Recipient, Message, Mailing


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
    fields = ['first_name', 'last_name', 'middle_name', 'email', 'comment']

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['first_name', 'last_name', 'middle_name', 'email', 'comment']

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    paginate_by = 20


class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    paginate_by = 20


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['started_date', 'ended_date', 'status', 'message', 'recipients']

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['started_date', 'ended_date', 'status', 'message', 'recipients']

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
