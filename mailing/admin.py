from django.contrib import admin

from mailing.models import Recipient, Message


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)
    readonly_fields = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    search_fields = ('subject', 'body',)
