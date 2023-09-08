from fastapi import Request

# Define the custom middleware
from starlette.middleware.base import BaseHTTPMiddleware


class JSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Call the next middleware or endpoint
        response = await call_next(request)

        # Set the Content-Type header to application/json
        response.headers["Content-Type"] = "application/json"

        return response
