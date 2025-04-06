import time

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone

from config.settings import CACHE_ENABLED
from mailing.models import MailingAttempt, Mailing, Recipient


class MailingService:
    """Сервис для работы с рассылками.
    Содержит методы для отправки писем и управления рассылками.
    """

    @staticmethod
    def send_mail_to_recipient(mailing, recipient):
        """Отправляет письмо одному получателю и создает запись о попытке отправки."""
        try:
            time.sleep(5)  # Задержка отправки 5 секунд, для отладки главной страницы
            send_mail(
                subject=mailing.message.subject,
                message='',
                html_message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            mailing_attempt = MailingAttempt(
                status=MailingAttempt.SUCCESSFULLY,
                mailing=mailing
            )
            mailing_attempt.save()
            return True
        except Exception as e:
            mailing_attempt = MailingAttempt(
                status=MailingAttempt.UNSUCCESSFULLY,
                response_mail_server=str(e),
                mailing=mailing
            )
            mailing_attempt.save()
            print(f'Ошибка отправки рассылки для получателя {recipient.email}: {str(e)}.')
            return False

    @staticmethod
    def send_mailing(mailing, force=False):
        """Запускает рассылку для всех получателей."""
        if mailing.status != mailing.CREATED and not force:
            raise ValueError('Данная рассылка уже запущена либо завершена.')

        if not mailing.started_date:
            mailing.started_date = timezone.now()
        mailing.status = mailing.LAUNCHED
        mailing.save()

        try:
            success_count = 0
            for recipient in mailing.recipients.all():
                if MailingService.send_mail_to_recipient(mailing, recipient):
                    success_count += 1
            mailing.ended_date = timezone.now()
            mailing.status = mailing.COMPLETED
            mailing.send_messages += 1
            mailing.save()
            return success_count
        except Exception as e:
            mailing.ended_date = timezone.now()
            mailing.status = mailing.CREATED
            mailing.save()
            raise e

    @staticmethod
    def get_recipients_list():
        """Возвращает список всех получателей с использованием кэширования."""
        if not CACHE_ENABLED:
            return Recipient.objects.all()

        key = 'recipients_list'
        recipients = cache.get(key)
        if not recipients:
            recipients = Recipient.objects.all()
            cache.set(key, recipients)
            return recipients
        return recipients


class StatisticsService:
    """Сервис для сбора статистики по рассылкам."""

    @staticmethod
    def get_mailing_count():
        """Возвращает общее количество рассылок."""
        mailing_count = Mailing.objects.all().count()
        return mailing_count

    @staticmethod
    def get_mailing_launched():
        """Возвращает количество запущенных рассылок."""
        mailing_launched = Mailing.objects.filter(status='launched').count()
        return mailing_launched

    @staticmethod
    def get_recipients_count():
        """Возвращает количество уникальных получателей."""
        recipients_count = Recipient.objects.values('email').distinct().count()
        return recipients_count

    @staticmethod
    def count_successfully_attempt(user):
        """Считает успешные попытки отправки для указанного пользователя."""
        return MailingAttempt.objects.filter(mailing__owner=user, status=MailingAttempt.SUCCESSFULLY).count()

    @staticmethod
    def count_unsuccessfully_attempt(user):
        """Считает неуспешные попытки отправки для указанного пользователя."""
        return MailingAttempt.objects.filter(mailing__owner=user, status=MailingAttempt.UNSUCCESSFULLY).count()

    @staticmethod
    def count_send_messages(user):
        """Считает общее количество отправленных сообщений пользователя по всем его рассылкам."""
        count = Mailing.objects.filter(owner=user).aggregate(total_sent=Sum('send_messages'))
        return count['total_sent'] or 0
