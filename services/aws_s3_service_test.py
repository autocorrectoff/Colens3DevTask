import unittest
import os
from .aws_s3_service import S3_Client
import boto3
from botocore.response import StreamingBody
from botocore.stub import Stubber
from datetime import datetime
from dateutil.tz import tzutc
from io import BytesIO
import hashlib

class TestS3_Client(unittest.TestCase):

    def setUp(self):
        os.environ["AWS_ACCESS_KEY"] = "dummy_access_key"
        os.environ["AWS_SECRET_KEY"] = "dummy_secret_key"
        self.client = boto3.client('s3')
        self.stubber = Stubber(self.client)

    def test_fetch_expect_success(self):
        response_body_content = b'file content'
        stream = BytesIO(response_body_content)
        get_object_response = {'ResponseMetadata': {'RequestId': '56E9A141DF38A831', 'HostId': 'OXLj68K2XbxQC7WZ735mYjM9Zz5mLv0wmsprBrrZCwVJQrGCZIZS3WAiPMQUMRpT8TYUV3tCgKc=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'OXLj68K2XbxQC7WZ735mYjM9Zz5mLv0wmsprBrrZCwVJQrGCZIZS3WAiPMQUMRpT8TYUV3tCgKc=', 'x-amz-request-id': '56E9A141DF38A831', 'date': 'Wed, 28 Oct 2020 14:59:23 GMT', 'last-modified': 'Fri, 25 Sep 2020 06:25:05 GMT', 'etag': '"607aecbe36e313cda319e8b2e54cd179"', 'accept-ranges': 'bytes', 'content-type': 'application/octet-stream', 'content-length': '14863', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'AcceptRanges': 'bytes', 'LastModified': datetime(2020, 9, 25, 6, 25, 5, tzinfo=tzutc()), 'ContentLength': 14863, 'ETag': '"607aecbe36e313cda319e8b2e54cd179"', 'ContentType': 'application/octet-stream', 'Metadata': {}, 'Body': StreamingBody(stream, len(response_body_content))}
        
        self.stubber.add_response('get_object', get_object_response, {"Bucket": "test_bucket", "Key": "path/to/file/test_file.txt"})
        expected = {
            "bucket_name": "test_bucket",
            "file_name": "test_file.txt",
            "timestamp": "10/28/2020, 12:04:36",
            "file_content_hash": hashlib.md5(response_body_content).hexdigest()
        }
        with self.stubber:
            client = S3_Client("test_bucket", self.client)
            result = client.fetch("path/to/file/test_file.txt")

        self.assertEqual(expected["bucket_name"], result["bucket_name"])
        self.assertEqual(expected["file_name"], result["file_name"])
        self.assertEqual(expected["file_content_hash"], result["file_content_hash"])

