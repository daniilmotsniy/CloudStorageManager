"""
this module contains storage API routes
"""

import typing
from os import environ
from uuid import uuid4
from pathlib import Path

import boto3
import aiofiles
from celery import chord
from bson import ObjectId
import motor.motor_asyncio
from starlette import status, responses
from google.cloud import storage
from fastapi import UploadFile, APIRouter, Depends

from cloud_storage_service.app.core.auth import get_current_active_user
from cloud_storage_service.app.models.storage import CreateBucketInput
from cloud_storage_service.app.models.user import User
from cloud_storage_service.app.worker import upload_to_s3, upload_to_cloud_storage, remove_tmp_file

storage_router = APIRouter(
    prefix="/api/storage",
    tags=["storage"],
    dependencies=[Depends(get_current_active_user)],
)

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(environ['MONGODB_URL'])
db = mongo_client.storage

aws_session = boto3.Session(region_name=environ.get('AWS_REGION', 'us-east-1'),
                            aws_access_key_id=environ['AWS_ACCESS_KEY'],
                            aws_secret_access_key=environ['AWS_SECRET_KEY'])
s3 = aws_session.client('s3')

gcp_storage_client = storage.client.Client()


@storage_router.post('/upload_file/', status_code=201)
async def upload_file(file: UploadFile, bucket_ids: typing.List[str],
                      current_user: User = Depends(get_current_active_user), folder: str = None):
    """
    file uploading for multiple buckets
    """

    bucket_ids = bucket_ids[0].split(',')
    bucket_q = {'_id': {'$in': [ObjectId(bucket_id) for bucket_id in bucket_ids]},
                'api_token': current_user.api_token}
    bucket_only = {'folders': 1, 'name': 1, 'provider': 1}
    if folder:
        buckets = [bucket async for bucket in db.buckets.aggregate([
            {
                '$match': bucket_q
            },
            {
                '$project': bucket_only
            },
            {
                '$unwind': '$folders'
            },
            {
                '$match': {'folders.name': folder}
            },
        ])]
    else:
        buckets = [bucket async for bucket in db.buckets.find(bucket_q, bucket_only)]

    if not buckets:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                      content={'error': 'You have no such bucket or folder!'})

    Path('../tmp').mkdir(parents=True, exist_ok=True)
    tmp_file_path = f'tmp/{uuid4()}-{file.filename}'
    async with aiofiles.open(tmp_file_path, 'wb') as out_file:
        content = await file.read()
        content_result = await out_file.write(content)

    tasks = []
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
                tasks.append(upload_to_cloud_storage.si(tmp_file_path,
                                                        db_bucket['name'], file.filename))
            else:
                return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                              content={'error': 'Unknown provider in bucket!'})

    upload_workflow = chord(*tasks, remove_tmp_file.si(tmp_file_path)).apply_async()
    return {'task_id': upload_workflow.id}


@storage_router.post('/folders', response_description='Add new folder')
async def create_folder(name: str, bucket: str, parent: str = None):
    """
    folder creation
    """
    created_folder = await db.buckets.update_one(
        {'_id': ObjectId(bucket)},
        {
            '$push': {
                'folders': {'name': name, 'parent': parent}
            }
        }
    )
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED,
                                  content={'acknowledged': created_folder.acknowledged})


@storage_router.post('/buckets', response_description='Add new bucket')
async def create_bucket(data: CreateBucketInput, current_user: User = Depends(get_current_active_user)):
    """
    bucket creation for selected provider
    """
    try:
        if data.provider.lower() == 'aws':
            s3.create_bucket(Bucket=data.name)
        elif data.provider.lower() == 'gcp':
            gcp_storage_client.create_bucket(data.name)
        else:
            return responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                          content={'error': 'There is wrong provider'})
    except ValueError as error:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                      content={'error': str(error)})
    new_bucket = await db.buckets.insert_one({
        'provider': data.provider,
        'name': data.name,
        'api_token': current_user.api_token,
        'folders': [],
        'files': [],
    })
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED,
                                  content={'_id': str(new_bucket.inserted_id)})


@storage_router.get('/bucket', response_description='Get bucket')
async def get_bucket(bucket_id: str, current_user: User = Depends(get_current_active_user)):
    """
    list of buckets
    """
    bucket = await db.buckets.find_one({'_id': ObjectId(bucket_id),
                                        'api_token': current_user.api_token}, {'_id': 0})
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=bucket)


@storage_router.get('/buckets', response_description='Get buckets')
async def get_buckets(current_user: User = Depends(get_current_active_user)):
    """
    get one bucket info
    """
    bucket_ids = [{'id': str(bucket['_id']), 'name': bucket['name'], 'provider': bucket['provider']}
                  async for bucket in db.buckets.find({'api_token': current_user.api_token},
                                                      {'_id': 1, 'name': 1, 'provider': 1})]
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=bucket_ids)
