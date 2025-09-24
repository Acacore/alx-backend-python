from datetime import datetime
from .models import *

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(message)s',
    handlers=[
        logging.FileHandler('request_logs.log')
    ]
)

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:

    def __init__(self,  get_response):
        self.get_response = get_response
        


    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

    