import os
from uuid import uuid4
from os import environ
from pathlib import Path

import aiofiles
import boto3
import motor.motor_asyncio
import uvicorn
from celery.result import AsyncResult
from fastapi import FastAPI, Body, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from models.storage import BucketModel, FolderModel
from models.user import UserModel
from worker import upload_to_s3

app = FastAPI()

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(environ["MONGODB_URL"])
db = mongo_client.storage

aws_session = boto3.Session(region_name='us-east-1',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                            aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
s3 = aws_session.client('s3')


@app.get("/tasks/{task_id}")
def get_status(task_id):
    """
    Allows to check status of celery task
    :param task_id: celery task id
    :return: processing status and result
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@app.post("/upload_file/", status_code=201)
async def upload_file(file: UploadFile, bucket: str, folder: str = None):
    Path("tmp").mkdir(parents=True, exist_ok=True)
    tmp_file_path = f'tmp/{uuid4()}-{file.filename}'
    async with aiofiles.open(tmp_file_path, 'wb') as out_file:
        content = await file.read()
        content_result = await out_file.write(content)
        db_file = await db["files"].insert_one({
            'name': file.filename,
            'bucket': bucket,
            'folder': folder,
        })
        if content_result:
            task = upload_to_s3.delay(tmp_file_path, bucket, file.filename, db_file.inserted_id)
    return {"task_id": task.id}


@app.post("/folders", response_description="Add new folder", response_model=FolderModel)
async def create_folder(folder: FolderModel = Body(...)):
    folder = jsonable_encoder(folder)
    new_folder = await db["folders"].insert_one(folder)
    created_folder = await db["folders"].find_one({"_id": new_folder.inserted_id})
    created_folder.pop('_id')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_folder)


@app.post("/buckets", response_description="Add new bucket", response_model=BucketModel)
async def create_bucket(provider: str, name: str):
    provider_db = await db["providers"].find_one({"name": provider})
    if not provider_db:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'error': 'There is no such provider'})
    if provider_db['name'].lower() == 'aws':
        try:
            s3.create_bucket(Bucket=name)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={'error': str(e)})
    elif provider.lower() == 'gcp':
        # TODO: create bucket GCP
        pass
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'error': 'There is wrong provider in database'})
    new_bucket = await db["buckets"].insert_one({
        'provider': provider,
        'name': name,
    })
    created_bucket = await db["buckets"].find_one({"_id": new_bucket.inserted_id})
    created_bucket.pop('_id')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_bucket)


@app.get("/bucket", response_description="Get bucket", response_model=BucketModel)
async def get_bucket(name: str):
    bucket = await db["buckets"].find_one({"name": name})
    bucket['_id'] = str(bucket['_id'])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=bucket)


@app.post("/users", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user['api_token'] = str(uuid4())
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    created_user.pop('_id')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@app.get("/")
async def root():
    return {"message": "Welcome to CloudStorageManager!"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8080, reload=True)
