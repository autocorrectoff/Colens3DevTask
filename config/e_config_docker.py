import os

e_config = {
    "aws_access_key": os.environ["AWS_ACCESS_KEY"],
    "aws_secret_key": os.environ["AWS_SECRET_KEY"],
    "redis_host": "redis_instance",
    "redis_port": 6379,
    "redis_password": ""
}