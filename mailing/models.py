from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

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
        ordering = ['last_name']


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
