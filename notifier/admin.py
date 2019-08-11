from django.contrib import admin

from .models import NotificationMessage, NotificationRoute


class NotificationMessageInline(admin.TabularInline):
    model = NotificationRoute
    extra = 0


@admin.register(NotificationMessage)
class NotificationMessageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'created_time', 'updated_time']
    search_fields = ['slug']
    inlines = [NotificationMessageInline]
