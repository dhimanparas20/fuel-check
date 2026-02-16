import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from modules.logger import get_logger, configure_uvicorn_filter
from routers import *

# os.system("clear")
load_dotenv()

logger = get_logger("APP")


# Define the FastAPI app with lifespan for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for FastAPI app."""
    try:
        pass

    except Exception as e:
        pass
    yield
    # Cleanup
    await FastAPILimiter.close()



app = FastAPI(
    title="Fuel Check API",
    description="API for fuel check authentication and management. Includes JWT authentication and agent query endpoints.",
    version="1.0.0",
    lifespan=lifespan,
    debug=os.getenv("DEBUG", "True").lower() in ("true", "1", "t"),
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=(["*"] if os.getenv("DEBUG", "False").lower() in ("true", "1", "t") else os.getenv("ALLOWED_HOSTS", "").split(",")),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=(["*"] if os.getenv("DEBUG", "False").lower() in ("true", "1", "t") else os.getenv("ALLOWED_ORIGINS", "").split(",")),
    allow_credentials=True,  # Set to True if your frontend sends cookies or authorization headers
    allow_methods=["*"],  # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers in the request
)

configure_uvicorn_filter()

# app.mount("/static", StaticFiles(directory="./server/static"), name="static")
# templates = Jinja2Templates(directory="./server/templates")

# Include routers
app.include_router(user_router, prefix="/user", tags=["User Operations"])
app.include_router(vehicle_router, prefix="/vehicle", tags=["Vehicle Operations"])
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction Operations"])


# Middleware to rewrite HTTP redirects to HTTPS
@app.middleware("http")
async def rewrite_http_to_https(request, call_next):
    response = await call_next(request)

    # Check if response is a redirect
    if response.status_code in [301, 302, 303, 307, 308] and "location" in response.headers:
        if response.headers["location"].startswith("http:"):
            response.headers["location"] = response.headers["location"].replace("http:", "https:", 1)

    return response


# Health check endpoint
@app.get(
    "/ping",
    summary="Ping",
    description="Health check endpoint.",
    response_class=JSONResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def ping():
    """Health check endpoint."""
    return JSONResponse({"ping": "pong"}, status.HTTP_200_OK)
