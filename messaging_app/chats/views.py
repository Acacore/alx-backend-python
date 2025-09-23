from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from .permissions import *
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from .pagination import *
from .message_filter import *



User = get_user_model()


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not a participant in this conversation."
    default_code = "forbidden"



class SignUpViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LoginViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializers = LoginSerializer(data=request.data, context={"request":request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        login(request, user)
        return Response({"status":"login in"}, status=status.HTTP_200_OK)
     
class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return self.queryset.filter(user_id=user)
    
    def perform_create(self, serializer):
        
        # Automatically set the user field to the authenticated
        serializer.save(user=self.request.user)


class PropertyViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return self.queryset.filter(user_id=user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated
        serializer.save(user=self.request.user)
   


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by("pk")
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = CustomPagination
    filterset_class = MessageFilter
    search_fields = ['message_body']   # assuming Message has a 'content' field
    ordering_fields = ['sender_id', 'sent_at']
    
   

   
    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return Message.objects.filter(conversation__participants_id=user.id)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated
        user = self.request.user
        conversation = serializer.validated_data["conversation"]
        conversation_id = conversation.conversation_id 

        if user not in conversation.participants_id.all():
            raise ForbiddenException(
                detail=f"You are not allowed to post in conversation {conversation_id}")
        
        serializer.save(sender_id=self.request.user, conversation=conversation)



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.order_by("pk")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = MessageFilter
    search_fields = ['message_body']   # assuming Message has a 'content' field
    ordering_fields = ['participants_id', 'created_at']


    def get_queryset(self):
        # Show only conversations where the authenticated user is the participant
        return self.queryset.filter(participants_id=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add the creator
        conversation.participants_id.add(self.request.user)

        # Add any other participants from the request
        extra_participants = self.request.data.get("participants", [])
        if extra_participants:
            conversation.participants_id.add(*extra_participants)
 
   
    


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return self.queryset.filter(user_id=user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return self.queryset.filter(user_id=user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated
        serializer.save(user=self.request.user)
