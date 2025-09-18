from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import uuid
from django.db.models import Deferrable, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE=[
        ("guess","Guess"),
        ("admin", "Admin"),
        ("host","Host")
    ]
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    email = models.EmailField(blank=False, null=False)
    phone_number = PhoneNumberField(blank=True)
    role = models.CharField(choices=ROLE, default=(ROLE[0][0]), max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, related_name='chats_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='chats_user_permissions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
        
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender_id.username} messaged {self.recipient_id.username}'

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now) 


class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField
    location = models.CharField(max_length=128)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updateted_at = models.DateTimeField(default=timezone.now)

    

    def __str__(self):
        return f'{self.host_id.username} owned {self.name}'
    
class Booking(models.Model):

    STATUS = [('pending','Pending'),
              ('confrimed', 'Confirmed'),
              ('canceled', 'Canceled')]
    
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=STATUS, default=STATUS[0][0], max_length=12)
    created_at = models.DateTimeField(default=models.CASCADE)

    def __str__(self):
        return f'{self.user_id.username} books {self.property_id.name}'

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f'{user_id.username} reviewed {property_id.name} with {rating}' 


class Payment(models.Model):
    STATUS = [('pending','Pending'),
              ('completed', 'Completed'),
              ('cancel','Canceld'),
              ('failed','Failed')]
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.URLField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=STATUS, default=STATUS[0][0], max_length=16)

    def __str__(self):
        return f'{self.user_id.username} paid {self.amount}'