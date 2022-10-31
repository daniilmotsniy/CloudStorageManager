import os
from uuid import uuid4
from os import environ
from pathlib import Path

import aiofiles
import boto3
import motor.motor_asyncio
import uvicorn
from bson import ObjectId
from celery.result import AsyncResult
from fastapi import FastAPI, UploadFile
from starlette import status
from starlette.responses import JSONResponse

from worker import upload_to_s3

app = FastAPI()

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(environ['MONGODB_URL'])
db = mongo_client.storage

aws_session = boto3.Session(region_name=os.environ.get('AWS_REGION', 'us-east-1'),
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                            aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
s3 = aws_session.client('s3')


@app.get('/tasks/{task_id}')
def get_status(task_id):
    """
    Allows to check status of celery task
    :param task_id: celery task id
    :return: processing status and result
    """
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result
    }
    return JSONResponse(result)


@app.post('/upload_file/', status_code=201)
async def upload_file(file: UploadFile, bucket_id: str, folder: str = None):
    db_bucket = await db['buckets'].find_one({'_id': ObjectId(bucket_id)},
                                             {'provider': 1, 'name': 1, 'folders': 1})
    if not bucket_id:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'error': 'You have no such bucket!'})
    # TODO validate folder
    Path('tmp').mkdir(parents=True, exist_ok=True)
    tmp_file_path = f'tmp/{uuid4()}-{file.filename}'
    async with aiofiles.open(tmp_file_path, 'wb') as out_file:
        content = await file.read()
        content_result = await out_file.write(content)
        # TODO add file URL
        await db['buckets'].update_one(
            {'_id': ObjectId(bucket_id)},
            {
                '$push': {
                    'files': {'name': file.filename, 'folder': folder}
                }
            }
        )
        if content_result:
            # TODO add mapper
            if db_bucket['provider'] == 'aws':
                task = upload_to_s3.delay(tmp_file_path, db_bucket['name'], file.filename)
            else:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content={'error': 'Unknown provider in bucket!'})
    return {'task_id': task.id}


@app.post('/folders', response_description='Add new folder')
async def create_folder(name: str, bucket: str, parent: str = None):
    created_folder = await db['buckets'].update_one(
        {'_id': ObjectId(bucket)},
        {
            '$push': {
                'folders': {'name': name, 'parent': parent}
            }
        }
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={'acknowledged': created_folder.acknowledged})


@app.post('/buckets', response_description='Add new bucket')
async def create_bucket(provider: str, name: str):
    provider_db = await db['providers'].find_one({'name': provider})
    if not provider_db:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'error': 'There is no such provider'})
    # TODO add mapper
    if provider_db['name'].lower() == 'aws':
        try:
            # FIXME the unspecified location constraint is incompatible
            #  for the region specific endpoint this request was sent to
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
    new_bucket = await db['buckets'].insert_one({
        'provider': provider,
        'name': name,
        'folders': [],
        'files': [],
    })
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'_id': str(new_bucket.inserted_id)})


@app.get('/bucket', response_description='Get bucket')
async def get_bucket(bucket_id: str):
    bucket = await db['buckets'].find_one({'_id': ObjectId(bucket_id)}, {'_id': 0})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=bucket)


@app.get('/')
async def root():
    return {'message': 'Welcome to CloudStorageManager!'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)
