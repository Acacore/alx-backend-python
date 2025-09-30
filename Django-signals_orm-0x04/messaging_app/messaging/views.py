from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets



# Create your views here.

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageViewSet():
    queryset = Message.objects.all()
    serializer_class =  MessagingSerializer

    class meta:
        ...