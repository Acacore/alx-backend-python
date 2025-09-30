from django.db import models
from django.contrib.auth import admin
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_messages")
     content = models.TextField()
     timestamp = models.DateTimeField(default=timezone.now)


