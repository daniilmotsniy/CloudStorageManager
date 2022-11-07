"""
this module contains all Celery tasks for uploading to cloud providers
"""


import os
import logging
import sys

import boto3
from celery import Celery
from google.cloud import storage

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

session = boto3.Session(region_name=os.environ.get('AWS_REGION', 'us-east-1'),
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                        aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
aws_s3_client = session.client('s3')
gcp_storage_client = storage.client.Client()

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


@celery.task(name="upload_to_s3")
def upload_to_s3(file_path, bucket, path):
    """
    upload to AWS S3 bucket
    """
    try:
        aws_s3_client.upload_file(file_path, bucket, path)
    except FileNotFoundError(file_path) as error:
        logging.error(error)
    return True


@celery.task(name="upload_to_cloud_storage")
def upload_to_cloud_storage(file_path, bucket, path):
    """
    upload to GCP Cloud Storage
    """
    try:
        bucket = gcp_storage_client.bucket(bucket)
        blob = bucket.blob(path)
        blob.upload_from_filename(file_path)
    except FileNotFoundError(file_path) as error:
        logging.error(error)
    return True


@celery.task(name="remove_tmp_file")
def remove_tmp_file(file_path):
    """
    removing temporary file after uploading
    """
    try:
        os.remove(file_path)
    except FileNotFoundError(file_path) as error:
        logging.error(error)
