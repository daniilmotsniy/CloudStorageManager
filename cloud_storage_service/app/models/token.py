from pydantic import BaseModel


class LoginInput(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
    tokenExp: str


class TokenData(BaseModel):
    username: str | None = None