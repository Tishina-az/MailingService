from django.core.management.base import BaseCommand

from mailing.models import Mailing
from mailing.services import MailingService


class Command(BaseCommand):
    help = 'Отправка рассылки сообщений'

    def add_arguments(self, parser):
        parser.add_argument(
            'mailing_id',
            type=int,
            help='ID рассылки сообщений'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная отправка, если рассылка уже запущена или завершена'
        )

    def handle(self, *args, **options):
        pk = options['mailing_id']
        force = options['force']

        try:
            mailing = Mailing.objects.get(pk=pk)
            if mailing.status != Mailing.CREATED and not force:
                self.stdout.write(self.style.WARNING(
                    f'Рассылка №{pk} уже запущена либо завершена. Используйте "--force" для принудительной отправки.'))
                return

            count = MailingService.send_mailing(mailing, force=force)
            self.stdout.write(
                self.style.SUCCESS(f'Рассылка №{pk} успешно отправлена! Получили рассылку: {count} из {mailing.recipients.count()} адресатов.'))
        except Mailing.objects.model.DoesNotExist:
            self.stderr.write(f"Рассылка №{pk} не найдена.")
        except Exception as e:
            self.stderr.write(f"Ошибка при отправке: {str(e)}.")
