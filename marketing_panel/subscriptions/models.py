from django.db import models

class UserAccess(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    expires_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username or self.full_name} ({self.telegram_id})"

