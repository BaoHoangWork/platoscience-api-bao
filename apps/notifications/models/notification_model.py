from django.db import models
from apps.users.models.user_model import User

class Notification(models.Model):
    
    title = models.CharField()
    description = models.CharField()
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        related_name='notifications', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    