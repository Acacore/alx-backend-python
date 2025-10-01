from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Message)
def message_sent(sender, instance, created, **kwargs):
    if created:
        print(f"A new Message has been sent to {instance.receiver}")