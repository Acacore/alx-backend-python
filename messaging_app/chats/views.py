from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters

from django.contrib.auth import get_user_model

User = get_user_model()






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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']   # assuming Message has a 'content' field
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Return onlly the message created by the authenticated user
        user = self.request.user
        return self.queryset.filter(sender_id=user.id)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated
        serializer.save(sender_id=self.request.user.id)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants_id__username']   # or 'participants__username' if not using _id
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Show only conversations where the authenticated user is the participant
        return self.queryset.filter(participants_id=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the participant to the authenticated user
        serializer.save(participants_id=self.request.user)
  
    
 

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
