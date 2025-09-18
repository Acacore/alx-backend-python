from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import re
from django.db.models import Avg


User = get_user_model()
class SignUpSeriliazer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ["first_name", "username", "last_name", "password","confirm_password",
                  "email", "phone_number", "role"]


    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password":"Passwords donot match"})
        
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        if not re.match(email_regex. data["email"]):
            raise serializers.ValidationError("Invalid email")
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(
            username = validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            role = validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]

        user = authenticate(username, password)
        if not user:
            raise serializers.ValidationError("Invalide credentials")
        data["user"] = user
        return data
class ReviewSeriliazer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields = '__all__'


class Messageeriliazer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSeriliazer(serializers.ModelSerializer):
   
    class Meta:
        model = Conversation
        fields = '__all__'

    
class BookingSeriliazer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSeriliazer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'



class ReviewSeriliazer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj,reviews.aggregate(avg=Avg("rating"))["avg"] or 0

class BookinSeriliazer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'