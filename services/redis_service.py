import redis
from config.e_config import e_config

class Redis_Client():

    def __init__(self):
        self.redis_client = redis.Redis(host=e_config["redis_host"], port=e_config["redis_port"], password=e_config["redis_password"])

    def fetch(self, key):
        binary_dict = self.redis_client.hgetall(key)
        str_response = { key.decode(): val.decode() for key, val in binary_dict.items() }
        return str_response

    def store(self, data):
        self.redis_client.hmset(data["bucket_name"], data)