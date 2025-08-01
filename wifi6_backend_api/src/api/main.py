from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.users import router as users_router
from src.api.devices import router as devices_router
from src.api.configs import router as configs_router

app = FastAPI(
    title="WiFi 6 Network Management API",
    description="API for managing and configuring WiFi 6 network devices",
    version="0.1.0",
    openapi_tags=[
        {"name": "users", "description": "User authentication and management"},
        {"name": "devices", "description": "WiFi 6 device management"},
        {"name": "configs", "description": "Network configuration management"},
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware to add security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    # PUBLIC_INTERFACE
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(users_router)
app.include_router(devices_router)
app.include_router(configs_router)

@app.get("/", tags=["health"], summary="Health Check", description="Check if the API is healthy", operation_id="health_check")
# PUBLIC_INTERFACE
def health_check():
    """Simple health check endpoint for the API."""
    return {"message": "Healthy"}
