from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Админ-панель для управления CustomUser."""
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
