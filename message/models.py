from django.db import models

from account.models import User


# Create your models here.
class Message(models.Model):

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )

    message_text = models.TextField(null=True, blank=True)
    
    is_popup = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    
    is_deleted_from_sender = models.BooleanField(default=False)
    is_deleted_from_receiver = models.BooleanField(default=False)
    
    is_delete = models.BooleanField(max_length=20, default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.sender)