from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .base import views

# FOR HEADER
def get_username(request):
    if request.user.is_authenticated:
        username = request.user.username
        show_login_register = False
    else:
        username = None
        show_login_register = True

    return {
        'username': username,
        'show_login_register': show_login_register,
    }
