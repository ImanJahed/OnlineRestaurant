
from . import models


class RequestObjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        
    def __call__(self, request):
        models.request_object = request
        
        response = self.get_response(request)

        return response