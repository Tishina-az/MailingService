from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientDeleteView, \
    RecipientUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path('', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/<int:pk>', RecipientDeleteView.as_view(), name='recipient_delete'),
]
