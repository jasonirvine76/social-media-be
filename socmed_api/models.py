from django.db import models
from django.utils import timezone
from datetime import date


from user_api.models import UserAccount
# Create your models here.

class Feed(models.Model):
    feed_msg = models.TextField(max_length=300)
    created_at = models.DateField(default = timezone.now(), null=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    visibility_to_close_friends = models.BooleanField(null=True)


    def __str__(self):
        return self.feed_msg
