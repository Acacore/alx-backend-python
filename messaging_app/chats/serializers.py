from .models import *
from rest_framework import serializers

class UserSeriliazer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        models = User
        fields = '__all__'


class ReviewSeriliazer(serializers.ModelSerializer):
   
    class Meta:
        models = Review
        fields = '__all__'


class Messageeriliazer(serializers.ModelSerializer):
    
    class Meta:
        models = Message
        fields = '__all__'

class ConversationSeriliazer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        models = Conversation
        fields = '__all__'

class BookingSeriliazer(serializers.ModelSerializer):

    class Meta:
        models = Booking
        fields = '__all__'


class PaymentSeriliazer(serializers.ModelSerializer):

    class Meta:
        models = Payment
        fields = '__all__'



class ReviewSeriliazer(serializers.ModelSerializer):

    class Meta:
        models = Review
        fields = '__all__'


class BookinSeriliazer(serializers.ModelSerializer):

    class Meta:
        models = Booking
        fields = '__all__'