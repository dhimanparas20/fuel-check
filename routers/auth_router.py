from fastapi import APIRouter, status, Header, HTTPException, Body
from fastapi.responses import JSONResponse

from models import user_model
from modules.jwt_util import *
from modules.logger import get_logger
from modules.utils import *

auth_router = APIRouter()
logger = get_logger("AUTH_ROUTER")


@auth_router.post(
    "/register",
    summary="Register a new user",
    description="Creates a new account.",
    status_code=status.HTTP_201_CREATED,
    response_description="Registration successful",
    response_class=JSONResponse,
)
async def register(user: user_model.CreateUserInput):
    """
    Register a new user.

    Parameters:
        user (CreateUser): Must include name, email, password.

    Returns:
        dict: Success message.
    """
    try:
        data = user.model_dump(exclude_unset=True)
        data["password"] = user_db.hashit(user.password)
        created_user = user_model.CreateUser(**data).model_dump()
        doc, created = user_db.get_or_create({"email": user.email}, created_user)
        print(doc)
        if not created:
            raise HTTPException(status_code=400, detail="Email already registered")
        return JSONResponse({"msg": "success", "user": user_model.ReadUser(**doc).model_dump()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Login for both Customer and Builder
@auth_router.post(
    "/login",
    summary="Login a user ",
    description="Authenticate a user and return a JWT token.",
    response_description="JWT token",
    response_class=JSONResponse,
)
async def login(login_data: user_model.LoginUser):
    """
    Login a user (customer or builder).

    Parameters:
        login_data (UserLogin): Must include email, password, and user_type.

    Returns:
        dict: JWT token.
    """
    email = login_data.email
    password = login_data.password

    user = user_db.get(filter={"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="User Not Found")
    if not user_db.verify_hash(password, user.get("password")):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    jwt_token = create_jwt_token(user=user)
    logger.debug("User logged in: %s", email)
    return JSONResponse(
        {"msg": "success","token": jwt_token},
        status_code=200,
    )



@auth_router.post(
    "/change-password",
    summary="Change user password",
    description="Change the password for a user",
    response_description="Password changed successfully",
    response_class=JSONResponse,
)
async def change_password(data: user_model.ChangePassword):
    """
    Change a user's password.

    Parameters:
        data (ChangePassword): Email, current password, and new password.

    Returns:
        dict: Success message.
    """

    user = user_db.get(filter={"email": data.email, "password": user_db.hashit(data.current_password)})
    if not user or not user_db.verify_hash(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_db.update_one({"email": data.email}, {"password": user_db.hashit(data.new_password)})
    logger.debug("Password reset for user: %s", data.email)
    return JSONResponse(
        {"msg": "success"},
        status_code=200,
    )



# Regenerate JWT Token
@auth_router.post(
    "/regenerate-token",
    summary="Regenerate JWT token ",
    description="Regenerate the JWT token for the authenticated user.",
    response_description="New JWT token",
    response_class=JSONResponse,
)
async def regenerate_token(
    x_token: str = Header(None, description="JWT token in 'x-token' header"),
):
    """
    Regenerate API key and JWT token.

    Parameters:
        x_token (str): JWT token in header.

    Returns:
        dict: New API key and JWT token.
    """
    # Use require_token to validate and get user
    _user = require_token(authorization=f"Bearer {x_token}")
    # Invalidate the old token (e.g., by updating a jwt_token_string)
    user_db.update_one({"id": _user["id"]}, {"jwt_token_string": user_db.gen_string(length=5)})
    # Generate new token with updated jwt_token_string
    new_jwt_token = create_jwt_token(_user)
    return JSONResponse(
        {"msg": "success","token": new_jwt_token},
        status_code=status.HTTP_201_CREATED,
    )