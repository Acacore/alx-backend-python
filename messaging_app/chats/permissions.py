from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''
        Custom permission to only allow users to access their own messages/conversations.
    '''
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user