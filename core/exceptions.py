import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "success": False,
                "error": {"code": exc.__class__.__name__, "message": str(exc)},
            },
            status=response.status_code,
        )

    logger.exception("Unhandled exception: %s", exc)

    return Response(
        {
            "success": False,
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred.",
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
