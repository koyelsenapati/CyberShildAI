"""
CyberShield AI
Logging Middleware
"""

import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("CyberShield")

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        process_time = round(
            time.time() - start,
            3,
        )

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{process_time}s"
        )

        return response
