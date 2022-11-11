from datetime import timedelta, datetime
from uuid import uuid4

from fastapi import Depends, HTTPException, status, APIRouter

from cloud_storage_service.app.models.token import Token, LoginInput
from cloud_storage_service.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from cloud_storage_service.app.core.auth import User, get_current_active_user, create_access_token, authenticate_user, create_user_in_mongo
from cloud_storage_service.app.models.user import RegisterUserInput, RegisterOutput

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@users_router.post("/register", response_model=RegisterOutput)
async def register(register_data: RegisterUserInput):

    user = register_data.username
    email = register_data.email
    pwd = register_data.password2
    api_token = str(uuid4())

    await create_user_in_mongo(user, email, pwd, api_token)

    return RegisterOutput(username=user, api_token=api_token)


@users_router.post("/token", response_model=Token)
async def login_for_access_token(data: LoginInput):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, token_exp_at = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires_delta
    )
    return {"token": access_token, "tokenExp": str(token_exp_at.timestamp())}


@users_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
