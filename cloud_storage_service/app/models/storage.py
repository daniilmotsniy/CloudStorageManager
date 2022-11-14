from pydantic import BaseModel


class CreateBucketInput(BaseModel):
    name: str
    provider: str
