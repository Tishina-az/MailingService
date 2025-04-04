from django.db import models

from users.models import CustomUser


class Recipient(models.Model):
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipients', verbose_name='Владелец')

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    @property
    def full_name(self):
        full_name = f'{self.last_name} {self.first_name}'
        if self.middle_name:
            full_name += f' {self.middle_name}'
        return full_name.strip()

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'owner'],
                name='unique_email_per_owner'
            )
        ]


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец')


    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['pk']


class Mailing(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'

    MAILING_STATUS = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    started_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    ended_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=9, choices=MAILING_STATUS, default=CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, related_name='mailings', verbose_name='Получатели')

    is_active = models.BooleanField(default=True, verbose_name='Включена/Отключена')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец')


    def __str__(self):
        return self.status

    def get_recipient_emails(self):
        """Получение списка адресатов рассылки"""
        return [recipient.email for recipient in self.recipients.all()]

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['pk']


class MailingAttempt(models.Model):
    """Модель 'Попытка рассылки' — это запись о каждой попытке отправки сообщения по рассылке"""

    SUCCESSFULLY = 'successfully'
    UNSUCCESSFULLY = 'unsuccessfully'

    ATTEMPT_STATUS = [
        (SUCCESSFULLY, 'Успешно'),
        (UNSUCCESSFULLY, 'Не успешно'),
    ]

    attempt_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=14, choices=ATTEMPT_STATUS, verbose_name='Статус попытки')
    response_mail_server = models.TextField(null=True, blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_attempts', verbose_name='Рассылка')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['-attempt_date']
