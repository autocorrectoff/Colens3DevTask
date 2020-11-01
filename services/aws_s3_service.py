import boto3
from config.e_config import e_config
from datetime import datetime
import hashlib

class S3_Client:

    def __init__(self, bucket_name, s3_client=None):
        if(s3_client == None):
            self.s3 = boto3.client("s3", aws_access_key_id=e_config["aws_access_key"], aws_secret_access_key=e_config["aws_secret_key"])
        else:
          self.s3 = s3_client  
        self.bucket_name = bucket_name

    def fetch(self, key):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)

        return self.__prepare_file_info(response, key)

    def fetch_all(self):
        response = self.s3.list_objects(Bucket=self.bucket_name)
        files_info = []
        for item in response["Contents"]:
            if(not item["Key"].endswith("/")):
                response = self.s3.get_object(Bucket=self.bucket_name, Key=item["Key"])
                file_info = self.__prepare_file_info(response, item["Key"])
                files_info.append(file_info)

        return files_info

    def __prepare_file_info(self, response, key):
        file_info = {}
        file_info["bucket_name"] = self.bucket_name
        key_parts = key.split("/")
        file_info["file_name"] = key_parts[len(key_parts) - 1]
        content = response['Body'].read()
        file_info["file_content_hash"] = hashlib.md5(content).hexdigest()
        file_info["timestamp"] = datetime.today().strftime("%m/%d/%Y, %H:%M:%S")

        return file_info