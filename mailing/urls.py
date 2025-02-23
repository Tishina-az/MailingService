from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientDeleteView, \
    RecipientUpdateView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/<int:pk>', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/message/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/mailing/update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
]
