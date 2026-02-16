from fastapi import APIRouter, Depends, status, Query, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
from fastapi.responses import StreamingResponse
from fastapi_limiter.depends import RateLimiter

from modules.logger import get_logger

user_router = APIRouter()
logger = get_logger("USER_ROUTER")