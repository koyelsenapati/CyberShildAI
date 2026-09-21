"""
CyberShield AI
Global Exception Handlers
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger("cybershield")

def register_exception_handlers(app: FastAPI):
    """
    Register global exception handlers.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        errors = []

        for error in exc.errors():
            error = error.copy()

            if isinstance(error.get("input"), bytes):
                error["input"] = error["input"].decode(
                    "utf-8",
                    errors="replace",
                )

            errors.append(error)

        logger.warning(
            "Validation error on %s %s: %s",
            request.method,
            request.url.path,
            errors,
        )

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "ValidationError",
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled exception on %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "detail": "An unexpected error occurred.",
            },
        )
