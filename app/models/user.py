from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    email: str | None = None
    api_token: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class RegisterUserInput(BaseModel):
    username: str
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


class RegisterOutput(BaseModel):
    username: str
    password: str
    api_token: str
