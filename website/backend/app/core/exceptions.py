from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class VibeAIError(Exception):
    """Base class for domain exceptions, mapped to clean HTTP responses."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Something went wrong."

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class NotFoundError(VibeAIError):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found."


class UnauthorizedError(VibeAIError):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "You need to sign in to do that."


class AIEngineUnavailableError(VibeAIError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    message = "VibeAI's reasoning engine is temporarily unavailable."


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(VibeAIError)
    async def handle_vibeai_error(request: Request, exc: VibeAIError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
