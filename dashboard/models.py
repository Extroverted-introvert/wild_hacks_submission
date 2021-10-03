from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SubscribedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.TextField(max_length=500, blank=True)
    prefered_time = models.CharField(max_length=30, blank=True)
    prefered_frequency = models.CharField(max_length=50, null=False, blank=True)
    next_message_time = models.DateTimeField(default = datetime.now )
    is_subscribed = models.BooleanField(null=False, default = False)