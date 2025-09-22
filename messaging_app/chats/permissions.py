from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''
        Custom permission to only allow users to access their own messages/conversations.
    '''
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user
    


class IsParticipantOfConversation(permissions.BasePermission):
    '''Allow any participants of converstation to access its messages'''

    def has_object_permission(self, request, view, obj):
        """
        obj could be a Message or a Conversation.
        Assumes:
          - Message has a conversation FK
          - Conversation has a ManyToManyField 'participants'
        """

        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        # if obj is a Message -> check conversation participants
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants_id.all()
        
        # if obj is a convesation -> check participant
        if hasattr(obj, "participants"):
            return user in obj.participants_id.all()
        
        return False
 