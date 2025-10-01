from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender')
    serializer_class = MessagingSerializer
    permission_classes = [IsAuthenticated]

    class meta:
        ...


def delete_user(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.pk)
        user.delete()

