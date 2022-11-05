from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    api_token: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Register:
    pass
