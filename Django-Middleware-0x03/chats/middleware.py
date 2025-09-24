from datetime import datetime, timedelta
from .models import *
from django.http import HttpResponseForbidden

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(message)s',
    handlers=[
        logging.FileHandler('requests.log')
    ]
)

logger = logging.getLogger(__name__)

now = datetime.now()
current_hour = now.hour
ini_time_for_now = now
# one_min_range = timedelta(min=1)

class RequestLoggingMiddleware:

    def __init__(self,  get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/messages/":
            if 18 < current_hour < 21:
                return HttpResponseForbidden("Message not allowed at this time")
            return self.respnse(request)

class OffensiveLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/messages/":
            messages = Message.objects.order_by('-sent_at')[:5]
            fith_message = messages[4]
            min = now.min
            time_range = now - fith_message.sent_at
            request = ""
        return self.get_response(request)

            

class RolepermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to perform this action")
        return self.get_response(request)

        



    