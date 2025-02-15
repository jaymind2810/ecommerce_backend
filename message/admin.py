from django.contrib import admin
from .models import Message

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    
    list_display = ('sender', 'receiver', 'is_read', 'is_delete', 'created_at')  # Add a custom method for total amount
    list_filter = ('sender', 'receiver',)
    search_fields = ('message_text',) 
    search_help_text="Search a message text."


admin.site.register(Message, MessageAdmin)

