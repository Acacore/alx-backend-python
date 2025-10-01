from .models import *
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class NotificationSerializer(serializers.ModelSerializer):
   
    class meta:
        models = Notification
        fields = ["message", "reciever", "content"]


class MessagingSerializer(serializers.ModelSerializer):
    message_history = serializers.SerializerMethodField()

    class meta:
        models = Message
        fields = ["sender", "reciever", "content", "message_history"]

    def get_message_history(self, obj):
       track =  MessageHistory.objects.filter(message=obj.pk)
       return MessageHistorySerializer(track, many=True).data


class MessageHistorySerializer(serializers.ModelSerializer):
    
    class meta:
        models = MessageHistory
        fields = ["message", "old_content"]