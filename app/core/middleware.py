import time

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from app.core.logger import logger


# Middleware that logs request lifecycle information
# and measures request processing performance.
class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        # Record request start time for performance measurement.
        start_time = time.time()

        # Log incoming request details.
        logger.info(
            f"Incoming request: "
            f"{request.method} {request.url.path}"
        )

        # Forward request to the next middleware/route handler.
        response = await call_next(request)

        # Calculate total processing time.
        process_time = time.time() - start_time

        # Log completed response details and execution duration.
        logger.info(
            f"Completed request: "
            f"{request.method} {request.url.path} "
            f"Status={response.status_code} "
            f"Duration={process_time:.4f}s"
        )

        return response