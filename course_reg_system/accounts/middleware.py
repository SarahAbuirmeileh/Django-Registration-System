from django.urls import reverse
from django.shortcuts import render, redirect

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if '_auth_user_id' not in request.session:
                return redirect(reverse('login'))
        response = self.get_response(request)
        return response