from django.conf import settings
from django.core.mail import send_mail


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
    except Exception as e:
        print(f'Ошибка отправки рассылки для получателя {recipient.email}: {str(e)}.')


def send_mailing(mailing):
    if mailing.status != mailing.CREATED:
        raise ValueError('Данная рассылка уже запущена либо завершена.')

    mailing.status = mailing.LAUNCHED
    mailing.save()

    try:
        success_count = 0
        for recipient in mailing.recipients.all():
            if send_mail_to_recipient(mailing, recipient):
                success_count += 1
        mailing.status = mailing.COMPLETED
        mailing.save()
        return success_count
    except Exception as e:
        mailing.status = mailing.CREATED
        mailing.save()
        raise e
