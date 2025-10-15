from datetime import datetime
from .models import *
from django.http import HttpResponseForbidden
from django.utils import timezone
from collections import defaultdict, deque

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
            
            else:
                return self.get_response(request)
        else:
            return self.get_response(request)


        
class OffensiveLanguageMiddleware:
    """
    Middleware that limits users (by IP address) to 5 messages per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store recent requests: {ip: deque([timestamps])}
        self.message_log = defaultdict(lambda: deque(maxlen=5))

    def __call__(self, request):
        # Only apply to POST requests to /messages/
        if request.path == "/messages/" and request.method == "POST":
            client_ip = self.get_client_ip(request)
            now = timezone.now()

            # Retrieve the log for this IP
            timestamps = self.message_log[client_ip]

            # If already 5 messages logged, check the time window
            if len(timestamps) == 5:
                # Oldest timestamp is at the left
                oldest = timestamps[0]
                time_diff = (now - oldest).total_seconds() / 60  # minutes

                if time_diff < 1:
                    return HttpResponseForbidden(
                        "Rate limit exceeded: only 5 messages per minute allowed."
                    )

            # Record the new timestamp
            timestamps.append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Extract client IP address from request headers.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

            

class RolepermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to perform this action")
        return self.get_response(request)

        



    