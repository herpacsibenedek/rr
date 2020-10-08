import logging

logger = logging.getLogger(__name__)
logger.info('Logger Started')


class LoggingMiddleware:
    """
    Logging middleware to log:
     - endpoint name
     - method type
     - request body
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        logger.info({
            "endpoint": request.get_full_path(),
            "method": str(getattr(request, 'method', '')).upper(),
            "request": "POST: " + str(getattr(request, 'POST', '')) + "GET: " + str(getattr(request, 'GET', ''))
        })

        return response
