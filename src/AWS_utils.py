import requests
import pandas as pd
import json
import logging
import boto3
from boto3.s3.transfer import S3Transfer
from botocore.exceptions import ClientError
from datetime import datetime

class AWSModule:

    s3=boto3.resource('s3')
    client= s3.meta.client
    transfer= S3Transfer(client)

    def __init__(self):
        pass

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True