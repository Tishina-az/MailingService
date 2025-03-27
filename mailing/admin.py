from django.contrib import admin
from django.utils.html import format_html

from mailing.models import Recipient, Message, Mailing, MailingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)
    readonly_fields = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'truncated_body',)
    search_fields = ('subject', 'body',)
    readonly_fields = ('display_body',)

    def truncated_body(self, obj):
        return format_html(obj.body[:200])
    truncated_body.short_description = "Текст (сокращенный)"

    def display_body(self, obj):
        return format_html(obj.body)  # Полный HTML-рендеринг
    display_body.short_description = "Текст письма"


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('started_date', 'ended_date', 'status', 'message',)
    readonly_fields = ('started_date', 'ended_date',)
    search_fields = ('message',)
    list_filter = ('status',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_date', 'status', 'response_mail_server', 'mailing',)
    readonly_fields = ('attempt_date', 'status', 'response_mail_server', 'mailing',)
    search_fields = ('mailing',)
    list_filter = ('status',)
