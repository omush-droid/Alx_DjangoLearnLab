from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'timestamp', 'read')
    list_filter = ('timestamp', 'read', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    readonly_fields = ('timestamp',)
