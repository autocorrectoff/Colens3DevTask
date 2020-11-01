from flask import Flask
from flask import request
from services.aws_s3_service import S3_Client
from services.redis_service import Redis_Client
import json

app = Flask(__name__)

@app.route("/load", methods = ['POST'])
def load():
    req_body = request.json
    s3_client = get_s3_client(req_body["bucket"])
    result = s3_client.fetch(key=req_body["key"])
    redis_client = get_redis_client()
    redis_client.store(result)

    response = {"status": "operation completed"}
    return json.dumps(response)

@app.route("/loadAll", methods = ['POST'])
def load_all():
    req_body = request.json
    s3_client = get_s3_client(req_body["bucket"])
    result = s3_client.fetch_all()
    for entry in result:
        redis_client = get_redis_client()
        redis_client.store(entry)

    response = {"status": "operation completed"}
    return json.dumps(response)

@app.route("/fetch", methods = ['POST'])
def fetch_by_bucket_name():
    req_body = request.json
    redis_client = get_redis_client()
    response = redis_client.fetch(req_body["bucket"])
    return json.dumps(response)

def get_s3_client(bucket_name):
    return S3_Client(bucket_name=bucket_name)

def get_redis_client():
    return Redis_Client()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")