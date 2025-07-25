from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed time range: from 6PM to 9PM
        self.allowed_start = time(18, 0)  # 6:00 PM
        self.allowed_end = time(21, 0)    # 9:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()
        if not (self.allowed_start <= current_time <= self.allowed_end):
            return HttpResponseForbidden("⛔ Access to messaging is restricted outside 6PM–9PM.")

        return self.get_response(request)

