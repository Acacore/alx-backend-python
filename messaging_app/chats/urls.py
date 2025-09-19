from django.urls import path, include
from .views import *
from .serializers import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'auth', LoginViewset, basename='auth')
router.register(r'signup', SignUpViewset, basename='signup')
router.register(r'review', ReviewViewset, 'review')
router.register(r'properties', PropertyViewset, 'properties')
router.register(r'messages', MessageViewSet, 'messages')
router.register(r'conversation', ConversationViewSet, 'conversation')
router.register(r'booking', BookingViewSet, 'booking')
router.register(r'payment', PaymentViewSet, 'payment')



urlpatterns = [
    path("", include(router.urls))
]
