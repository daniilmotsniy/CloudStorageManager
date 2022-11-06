from datetime import timedelta
from uuid import uuid4

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter

from app.models.token import Token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.auth import User, get_current_active_user, create_access_token, authenticate_user, create_user_in_mongo
from app.models.user import RegisterUserInput, RegisterOutput

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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
