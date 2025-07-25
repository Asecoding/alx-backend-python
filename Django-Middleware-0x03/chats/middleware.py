# messaging_app/middleware.py
import logging
from datetime import datetime
from datetime import datetime, time
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='request_logs.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response


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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize or clean up timestamps
            timestamps = self.ip_tracker.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < timedelta(minutes=1)]

            if len(timestamps) >= 5:
                return HttpResponseForbidden("⛔ Rate limit exceeded: Max 5 messages per minute.")

            timestamps.append(now)
            self.ip_tracker[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "")

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Skip if the user is not authenticated
        if not user.is_authenticated:
            return HttpResponseForbidden("⛔ You must be logged in to access this resource.")

        # Customize this logic to your role field/permissions model
        if not user.is_superuser and not getattr(user, 'role', '') in ['admin', 'moderator']:
            return HttpResponseForbidden("⛔ Access denied: insufficient permissions.")

        return self.get_response(request)
