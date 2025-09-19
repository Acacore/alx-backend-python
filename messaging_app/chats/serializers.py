from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Avg
import uuid



User = get_user_model()
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type':'password'})
    confirm_password = serializers.CharField(write_only=True, min_length=8, style={'input_type':'password'})
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name",
                  "last_name", "email",
                  "password","confirm_password",
                  "phone_number", "role"]


    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password":"Passwords donot match"})

        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]

       
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username )
            if not user:
                raise serializers.ValidationError("Invalide credentials")
            else:
                raise serializers.ValidationError("Must include 'username' and 'password")
        data["user"] = user
        return data
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ReviewSerializer(serializers.ModelSerializer):
   user_id = UserSerializer(read_only=True)

   class Meta:
        model = Review
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    user_id = UserSerializer(read_only=True)
    
    
    class Meta:
        model = Property
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg("rating"))["avg"] or 0



class MessageSerializer(serializers.ModelSerializer):
    user = LoginSerializer(read_only=True)
    message_id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)
    user_id = UserSerializer(read_only=True)
   
    class Meta:
        model = Conversation
        fields = '__all__'

    
class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.UUIDField(read_only=True)
    user_id = UserSerializer(read_only=True)


    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_id = serializers.UUIDField(read_only=True)
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

   

class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.UUIDField(read_only=True)
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'

    

