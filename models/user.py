from bson import ObjectId
from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    password: str

    class Config:
        json_encoders = {ObjectId: str}

