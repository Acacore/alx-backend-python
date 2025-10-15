from django.urls import path, include
from .views import *
from .serializers import *
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages inside a conversation
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')
router.register(r'auth', LoginViewset, basename='auth')
router.register(r'signup', SignUpViewset, basename='signup')
router.register(r'review', ReviewViewset, 'review')
router.register(r'properties', PropertyViewset, 'properties')
router.register(r'booking', BookingViewSet, 'booking')
router.register(r'payment', PaymentViewSet, 'payment')



urlpatterns = [
    path("", include(router.urls))
]
