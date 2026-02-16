import os
from datetime import datetime, UTC, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Header, Request
from entity import user_db
from modules.logger import get_logger

load_dotenv()
logger = get_logger("SERVER_UTILS")
SECRET = os.getenv("JWT_SECRET", "superse345cret67")


# Utility functions for JWT token creation and validation
def create_jwt_token(user: dict) -> str:
    """Create a JWT token for a user."""
    payload = {
        "id": user.get("id"),
        "name": user.get("full_name"),
        "email": user.get("email"),
        "jwt_token_string": user.get("jwt_token_string"),
        "exp": datetime.now(UTC) + timedelta(days=7),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_jwt_token(token: str) -> dict:
    """Decode a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token.")
        raise HTTPException(status_code=401, detail="Invalid token.")


def get_user_from_token(token: str) -> dict:
    """Extract user info from JWT token and ensure token is still valid (not superseded)."""
    payload = decode_jwt_token(token)
    user = user_db.get_by_id(id=payload["id"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token.")
    elif not user.get("is_active"):
        raise HTTPException(status_code=401, detail="User account not active.")
    # Check if the jwt_token_string in the token matches the one in the database
    if user.get("jwt_token_string") != payload.get("jwt_token_string"):
        raise HTTPException(status_code=401, detail="Token has been invalidated. Please login again.")
    return user


def get_token_from_header(authorization: str = Header(...)) -> str:
    """Extract token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header.")
    return authorization.split(" ", 1)[1]


# FastAPI dependency to require and validate JWT token
def require_token(authorization: str = Header(None, description="JWT token in 'Authorization' header")) -> dict:
    """FastAPI dependency to require and validate JWT token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        logger.error("Authorization header with Bearer token required")
        raise HTTPException(status_code=401, detail="Authorization header with Bearer token required")
    token = authorization.split(" ", 1)[1]
    return get_user_from_token(token)
