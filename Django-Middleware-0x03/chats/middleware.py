from datetime import datetime
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

class RequestLoggingMiddleware:

    def __init__(self,  get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        if request.path == "/messages/":
            if 18 < current_hour < 21:
                return HttpResponseForbidden("Message not allowed at this time")
            return self.get_request(request)