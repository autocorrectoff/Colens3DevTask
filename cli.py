import argparse
import json
from services.aws_s3_service import S3_Client
from services.redis_service import Redis_Client

def load(bucket, key):
    if(bucket == None or key == None):
        print("bucket and key arguments are required.")
        return

    s3_client = get_s3_client(bucket)
    result = s3_client.fetch(key)
    redis_client = get_redis_client()
    redis_client.store(result)

    response = {"status": "operation completed"}
    return json.dumps(response)

def load_all(bucket):
    if(bucket == None):
        print("bucket argument is required.")
        return

    s3_client = get_s3_client(bucket)
    result = s3_client.fetch_all()
    for entry in result:
        redis_client = get_redis_client()
        redis_client.store(entry)

    response = {"status": "operation completed"}
    return json.dumps(response)

def fetch_from_db(bucket):
    if(bucket == None):
        print("bucket argument is required.")
        return

    redis_client = get_redis_client()
    response = redis_client.fetch(bucket)
    return json.dumps(response)

def get_s3_client(bucket_name):
    return S3_Client(bucket_name=bucket_name)

def get_redis_client():
    return Redis_Client()

def start():
    default_option = None
    default_bucket = None
    default_key = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-option", type=str, default=default_option, action="store", dest="option")
    parser.add_argument("-bucket", type=str, default=default_bucket, action="store", dest="bucket")
    parser.add_argument("-key", type=str, default=default_key, action="store", dest="key")

    args = parser.parse_args()

    if(args.option == None):
        print("option argument is required. Possible values: load | loadAll | fetch")
        return
    
    if(args.option == "load"):
        print(load(args.bucket, args.key))

    if(args.option == "loadAll"):
        print(load_all(args.bucket))

    if(args.option == "fetch"):
        print(fetch_from_db(args.bucket))

if __name__ == "__main__":
    start()