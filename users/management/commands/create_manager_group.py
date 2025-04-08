from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджер" и назначает ей необходимые разрешения'

    def handle(self, *args, **options):
        group, create = Group.objects.get_or_create(name='Менеджер')

        if create:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджер" успешно создана.'))

            view_recipient_permission = Permission.objects.get(codename='view_recipient')
            view_message_permission = Permission.objects.get(codename='view_message')
            view_mailing_permission = Permission.objects.get(codename='view_mailing')
            view_users_permission = Permission.objects.get(codename='view_customuser')
            block_users_permission = Permission.objects.get(codename='can_block_user')
            unblock_users_permission = Permission.objects.get(codename='can_unblock_user')
            disable_mailing_permission = Permission.objects.get(codename='can_disable_mailing')
            enable_mailing_permission = Permission.objects.get(codename='can_enable_mailing')

            group.permissions.add(view_mailing_permission, view_users_permission, view_recipient_permission,
                                  view_message_permission, block_users_permission, unblock_users_permission,
                                  disable_mailing_permission, enable_mailing_permission)
            self.stdout.write(self.style.SUCCESS('Группе "Менеджер" успешно назначены разрешения'))

        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджер" уже существует.'))
