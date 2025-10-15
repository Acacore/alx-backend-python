from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import *
from django.shortcuts import get_object_or_404

# @receiver(post_save, sender=Message)
# def message_sent(sender, instance, created, **kwargs):
#     if created:
#         print(f"A new Message has been sent to {instance.receiver}")



@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def create_messageHistory(sender, instance, **kwargs):

    try:
        if Message.objects.get(pk=instance.pk):
            MessageHistory.objects.create(
                old_content = instance.content,
                message=instance
            )
            instance.edited = True
            
    except Message.DoesNotExist:
        return

@receiver(post_delete, sender=User)
def delete_account(sender, instance, **kwargs):
    user_messages = Message.objects.filter(sender=instance.pk)
    user_messages.delete()
        
