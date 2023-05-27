from django.db import connections
from django.contrib.auth.models import User


class DatabaseSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser:
            connections['default'].alias = 'admin'
        else:
            connections['default'].alias = 'default'

        return self.get_response(request)