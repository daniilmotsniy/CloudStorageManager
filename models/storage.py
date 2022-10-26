import typing

from bson import ObjectId
from pydantic import BaseModel


class FolderModel(BaseModel):
    name: str
    parent: str = None
    bucket: str

    class Config:
        json_encoders = {ObjectId: str}


class BucketModel(BaseModel):
    provider: str
    name: str
    files: typing.List
    folders: typing.List[FolderModel]

    class Config:
        json_encoders = {ObjectId: str}
