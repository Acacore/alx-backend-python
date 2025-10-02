from django.db import models

class UnreadMessageManager(models.Manager):
    def unread_for_user(self, user):
        return super().get_queryset().filter(reciever=user, read=False)
