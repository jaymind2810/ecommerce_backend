from django.db import models
from account.models import User


# Create your models here.
class Notification(models.Model):
    OTHER_NOTIFICATION = 'other_notification'
    MESSAGE_RECEIVED = 'message_received'

    NOTIFICATION_TYPES = (
        (OTHER_NOTIFICATION, 'Other Notification'),
        (MESSAGE_RECEIVED, 'Message Received'),
    )
    
    notifyBy = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='Notify_By')
    notifyTo = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Notify_To')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='other_notification')

    is_popup = models.BooleanField(default=False)
    is_view = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)


    is_delete = models.BooleanField(max_length=20, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ("-created_at",)