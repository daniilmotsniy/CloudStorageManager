import os
import typing
from uuid import uuid4
from os import environ
from pathlib import Path

import aiofiles
import boto3
import motor.motor_asyncio
import uvicorn
from bson import ObjectId
from celery import chord
from celery.result import AsyncResult
from fastapi import FastAPI, UploadFile
from starlette import status
from starlette.responses import JSONResponse

from worker import upload_to_s3, remove_tmp_file

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
async def upload_file(file: UploadFile, bucket_ids: typing.List[str], folder: str = None):
    buckets = [bucket async for bucket in db.buckets.aggregate([
        {
            '$match': {'_id': {'$in': [ObjectId(bucket_id) for bucket_id in bucket_ids]}}
        },
        {
            '$project': {'folders': 1, 'name': 1, 'provider': 1}
        },
        {
            '$unwind': '$folders'
        },
        {
            '$match': {'folders.name': folder}
        },
    ])]
    if not buckets:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'error': 'You have no such bucket or folder!'})

    Path('tmp').mkdir(parents=True, exist_ok=True)
    tmp_file_path = f'tmp/{uuid4()}-{file.filename}'
    async with aiofiles.open(tmp_file_path, 'wb') as out_file:
        content = await file.read()
        content_result = await out_file.write(content)

    tasks = list()
    for db_bucket in buckets:
        await db.buckets.update_one(
            {'_id': ObjectId(db_bucket['_id'])},
            {
                '$push': {
                    'files': {'name': file.filename, 'folder': folder}
                }
            }
        )
        if content_result:
            if db_bucket['provider'] == 'aws':
                tasks.append(upload_to_s3.si(tmp_file_path, db_bucket['name'], file.filename))
            elif db_bucket['provider'] == 'gcp':
                pass
            else:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content={'error': 'Unknown provider in bucket!'})

    upload_workflow = chord(*tasks, remove_tmp_file.si(tmp_file_path)).apply_async()
    return {'task_id': upload_workflow.id}


@app.post('/folders', response_description='Add new folder')
async def create_folder(name: str, bucket: str, parent: str = None):
    created_folder = await db.buckets.update_one(
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
    new_bucket = await db.buckets.insert_one({
        'provider': provider,
        'name': name,
        'folders': [],
        'files': [],
    })
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'_id': str(new_bucket.inserted_id)})


@app.get('/bucket', response_description='Get bucket')
async def get_bucket(bucket_id: str):
    bucket = await db.buckets.find_one({'_id': ObjectId(bucket_id)}, {'_id': 0})
    return JSONResponse(status_code=status.HTTP_200_OK, content=bucket)


@app.get('/buckets', response_description='Get buckets')
async def get_buckets():
    bucket_ids = [{'id': str(bucket['_id']), 'name': bucket['name']}
                  async for bucket in db.buckets.find({}, {'_id': 1, 'name': 1})]
    return JSONResponse(status_code=status.HTTP_200_OK, content=bucket_ids)


@app.get('/')
async def root():
    return {'message': 'Welcome to CloudStorageManager!'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)
