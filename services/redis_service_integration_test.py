import unittest
from .redis_service import Redis_Client
import redis
from config.e_config import e_config

# in order to to run this integration test you should have a Redis instance running
class TestRedis_Client(unittest.TestCase):

    def setUp(self):
        self.redis_client = redis.Redis(host=e_config["redis_host"], port=e_config["redis_port"], password=e_config["redis_password"])
        self.sample_data = {
            "bucket_name": "test_bucket",
            "file_name": "test_file.txt",
            "timestamp": "10/28/2020, 12:04:36",
            "file_content_hash": "1234"
        }
        self.redis_client.hmset("test_bucket", self.sample_data)

    def tearDown(self):
        self.redis_client.delete("test_bucket")

    def test_fetch_expect_success(self):
        redis_client = Redis_Client()
        response = redis_client.fetch("test_bucket")
        self.assertDictEqual(response, self.sample_data)
