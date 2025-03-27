from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import MailingAttempt


class MailingService:

    @staticmethod
    def send_mail_to_recipient(mailing, recipient):
        try:
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
        if mailing.status != mailing.CREATED and not force:
            raise ValueError('Данная рассылка уже запущена либо завершена.')

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
            mailing.save()
            return success_count
        except Exception as e:
            mailing.ended_date = timezone.now()
            mailing.status = mailing.CREATED
            mailing.save()
            raise e
