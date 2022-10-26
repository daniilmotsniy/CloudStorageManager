import os

import boto3
from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

session = boto3.Session(region_name='us-east-1',
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                        aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
client = session.client('s3')


@celery.task(name="upload_to_s3")
def upload_to_s3(file_path, bucket, path):
    try:
        client.upload_file(file_path, bucket, path)
        os.remove(file_path)
    except FileNotFoundError(file_path) as e:
        print(e)
    return True
