from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mailing.forms import RecipientForm, MessageForm, MailingForm, MailingUpdateForm
from mailing.models import Recipient, Message, Mailing, MailingAttempt
from mailing.services import MailingService, StatisticsService


class RecipientListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка получателей рассылки."""
    model = Recipient
    template_name = "recipient_list"
    context_object_name = "recipients"
    paginate_by = 10

    def get_queryset(self):
        """Возвращает queryset получателей в зависимости от роли пользователя."""
        if self.request.user.groups.filter(name="Менеджер").exists():
            return MailingService.get_recipients_list()
        return MailingService.get_recipients_list().filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового получателя."""
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешного создания."""
        return reverse_lazy("mailing:recipient_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        """Добавляет request в kwargs формы."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Устанавливает владельца получателя перед сохранением."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name="dispatch")
class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Представление для детального просмотра получателя с кэшированием на 15 минут."""
    model = Recipient
    context_object_name = "recipient"

    def get_object(self, queryset=None):
        """Проверяет права доступа к получателю."""
        obj = super().get_object(queryset)
        if not (obj.owner == self.request.user or self.request.user.has_perm("mailing.view_recipient")):
            raise PermissionDenied("У вас не достаточно прав для просмотра данной страницы.")
        return obj


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования получателя."""
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy("mailing:recipient_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Проверяет права на редактирование перед сохранением."""
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для редактирования данного клиента.")
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления получателя."""
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

    def get_object(self, queryset=None):
        """Проверяет права на удаление."""
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для удаления данного клиента.")
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    """Представление для списка сообщений."""
    model = Message
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        """Фильтрует сообщения по правам доступа."""
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр дельной информации о сообщении с кэшированием."""
    model = Message
    context_object_name = "message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (obj.owner == self.request.user or self.request.user.has_perm("mailing.view_message")):
            raise PermissionDenied("У вас не достаточно прав для просмотра данной страницы.")
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения."""
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        obj = self.get_object()

        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для редактирования данного сообщения.")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения."""
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для удаления данного сообщения.")
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка рассылок."""
    model = Mailing
    context_object_name = "mailings"
    paginate_by = 10

    def get_queryset(self):
        """Фильтрует рассылки по правам доступа."""
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user, is_active=True)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр дельной информации о рассылке с кэшированием."""
    model = Mailing
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (obj.owner == self.request.user or self.request.user.has_perm("mailing.view_mailing")):
            raise PermissionDenied("У вас не достаточно прав для просмотра данной страницы.")
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки."""
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class=None):
        """Фильтрует доступные сообщения и получателей."""
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.filter(owner=self.request.user)
        form.fields["recipients"].queryset = Recipient.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование рассылки."""
    model = Mailing
    form_class = MailingUpdateForm

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.filter(owner=self.request.user)
        form.fields["recipients"].queryset = Recipient.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для редактирования данной рассылки.")
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки."""
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для удаления данной рассылки.")
        return obj


class DisableMailingView(LoginRequiredMixin, View):
    """Отключение рассылки (требует специального разрешения)."""

    def post(self, request, pk):
        disable_mailing = get_object_or_404(Mailing, pk=pk)

        if self.request.user.has_perm("mailing.can_disable_mailing"):
            disable_mailing.is_active = False
            disable_mailing.save()
            return redirect(reverse("mailing:mailing_list"))
        else:
            raise PermissionDenied("У вас не достаточно прав для отключения рассылки.")


class EnableMailingView(LoginRequiredMixin, View):
    """Включение рассылки (требует специального разрешения)."""

    def post(self, request, pk):
        disable_mailing = get_object_or_404(Mailing, pk=pk)

        if self.request.user.has_perm("mailing.can_enable_mailing"):
            disable_mailing.is_active = True
            disable_mailing.save()
            return redirect(reverse("mailing:mailing_list"))
        else:
            raise PermissionDenied("У вас не достаточно прав для включения рассылки.")


class SendMailingView(LoginRequiredMixin, View):
    """Ручной запуск рассылки."""

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.owner == self.request.user:
            try:
                count = MailingService.send_mailing(mailing)
                messages.success(
                    request,
                    f"Рассылка №{pk} успешно отправлена: {count} из {mailing.recipients.count()} адресатам.",
                )
            except Exception as e:
                messages.error(request, f"Ошибка при отправке: {str(e)}")
            return redirect(reverse("mailing:mailing_detail", kwargs={"pk": pk}))
        else:
            raise PermissionDenied("У вас не достаточно прав для отправки данной рассылки.")


class MainPageView(TemplateView):
    """Главная страница с общей статистикой."""
    template_name = "mailing/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_count"] = StatisticsService.get_mailing_count()
        context["mailing_launched"] = StatisticsService.get_mailing_launched()
        context["recipients_count"] = StatisticsService.get_recipients_count()
        return context


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """Список попыток рассылки для текущего пользователя."""
    model = MailingAttempt
    template_name = "mailing/mailing_attempt_list.html"
    context_object_name = "mailing_attempts"
    paginate_by = 20

    def get_queryset(self):
        return MailingAttempt.objects.filter(mailing__owner=self.request.user).select_related("mailing")


class StatisticsView(LoginRequiredMixin, TemplateView):
    """Страница персональной статистики пользователя."""
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["successfully_attempt"] = StatisticsService.count_successfully_attempt(user)
        context["unsuccessfully_attempt"] = StatisticsService.count_unsuccessfully_attempt(user)
        context["count_messages"] = StatisticsService.count_send_messages(user)
        return context
