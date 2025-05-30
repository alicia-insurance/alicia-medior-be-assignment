import logging
import time
import traceback

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("api_logger")


class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs API requests and responses.
    This middleware captures the start time of each request, calculates the duration of the request processing,
    and logs relevant information such as HTTP method, path, user, response status code, duration, and client IP address.
    Methods:
        process_request(request):
            Stores the start time of the request for duration calculation.
        process_response(request, response):
            Calculates the duration of the request, retrieves user and client IP information,
            and logs the request and response details.
        get_client_ip(request):
            Retrieves the client's IP address from the request headers, considering possible proxy headers.
    """

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, "start_time", time.time())
        user = (
            request.user.username
            if getattr(request, "user", None) and request.user.is_authenticated
            else "Anonymous"
        )
        ip = self.get_client_ip(request)

        logger.info(
            {
                "method": request.method,
                "path": request.get_full_path(),
                "user": str(user),
                "status": response.status_code,
                "duration": f"{duration:.3f}s",
                "ip": ip,
            }
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def process_exception(self, request, exception):
        logger.error(
            {
                "method": request.method,
                "path": request.get_full_path(),
                "user": str(getattr(request.user, "username", "Anonymous")),
                "ip": self.get_client_ip(request),
                "exception": str(exception),
                "traceback": traceback.format_exc(),
            }
        )
