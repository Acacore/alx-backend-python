from django.shortcuts import render
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.contrib.auth.decorators import login_required

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


def fetch_thread(root_message):
    # 1. Pull all descendants in one query (or even all messages in the conversation)
    all_messages = (
        Message.objects.filter(parent_message__isnull=False)   # all replies in DB
        .select_related("sender", "receiver", "parent_message")  # avoids FK lookups
    )

    # 2. Group by parent_message_id (so we can build tree in memory)
    children_map = defaultdict(list)
    for msg in all_messages:
        children_map[msg.parent_message_id].append(msg)

    # 3. Recursive builder using the in-memory map
    def build_tree(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "children": [build_tree(child) for child in children_map[message.id]]
        }

    return build_tree(root_message)

    
def delete_user(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.pk)
        user.delete()

@login_required
def user_message(request):
    if request.user.is_authenticated:
        messages = Message.objects.select_related("sender").filter(sender=request.user)
        data = list(messages.values)
        return JsonResponse(data, safe=False)
    

@login_required   
def unread_message(request):
    if request.user.is_authenticated():
        user = request.user
        return Message.unread.unread_for_user(user).only('content', 'timestamp')
