from datetime import datetime, timedelta
from os import environ

import motor.motor_asyncio
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import SECRET_KEY, ALGORITHM
from app.models.token import TokenData
from app.models.user import UserInDB, User


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(environ['MONGODB_URL'])
db = mongo_client.storage


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user_dict = await db.users.find_one({'username': username}, {'_id': 0})
    user = UserInDB(**user_dict)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_user_in_mongo(username: str, email: str, password: str, api_token: str):
    await db.users.insert_one({
        'username': username,
        'email': email,
        'hashed_password': get_password_hash(password),
        'api_token': api_token,
        'disabled': False,
    })


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_dict = await db.users.find_one({'username': token_data.username}, {'_id': 0})
    user = UserInDB(**user_dict)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
