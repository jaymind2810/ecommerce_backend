from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'notification_type', 'notifyBy', 'notifyTo', 'is_read')  # Add a custom method for total amount
    list_filter = ('notification_type', 'notifyBy', 'notifyTo',)
    search_fields = ('title', 'description',) 
    search_help_text="Search a notification title"


admin.site.register(Notification, NotificationAdmin)

