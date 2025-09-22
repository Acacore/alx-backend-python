from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that lets users log in with either
    their username OR their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Accept both username and email as login fields
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

