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

    def create(self, request):
        sender = request.user
        receiver = request.data.get('receiver')
        Message.objects.filter(receiver=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender, receiver=receiver)


def fetch_replies(message):
    replies = []
    children = Message.objects.filter(parent_message=message)
    for child in children:
        replies.append({
            "id": child.id,
            "sender": child.sender.username,
            "content": child.content,
            "timestamp": child.timestamp,
            "children": fetch_replies(child)  # recursion
        })
    return replies
    
def delete_user(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.pk)
        user.delete()

