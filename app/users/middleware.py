
from django.contrib.auth import logout
from django.conf import settings
from datetime import datetime, timedelta

from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity and (datetime.now() - datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S") 
                                > timedelta(seconds=settings.SESSION_COOKIE_AGE)):
                logout(request)
                del request.session['last_activity']
                return redirect('users:login')  # или другая страница
            
            request.session['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        response = self.get_response(request)
        return response