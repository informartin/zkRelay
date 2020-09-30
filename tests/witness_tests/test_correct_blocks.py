import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer

BATCH_SIZE=2

# Mock Click.Context object that is normally passed through cli to functions 
class Context:
    obj = {}

class TestWitnessCorrectBlocks(unittest.TestCase):

    def setUp(self):
        self.ctx = Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_2_blocks(self):
        host = self.ctx.obj.get('bitcoin_client').get('host')
        port = self.ctx.obj.get('bitcoin_client').get('port')

        # get json config for test case
        fd = open('./tests/test_data/test_witness/test_correct_blocks/2_blocks.json', 'r')
        config = json.load(fd)
        fd.close()

        with HTTPServer(host=host, port=port) as httpserver:
            for http_response in config.get('http_responses'):
                httpserver.expect_ordered_request('/').respond_with_json(http_response)
            preprocessing.validateBatchFromBlockNo(self.ctx,
                                                1, 
                                                2)

    # def test_correct_blocks_online(self):
    #     self.ctx.obj = toml.load('./tests/conf/online_conf.toml')

    #     preprocessing.validateBatchFromBlockNo(self.ctx,
    #                                             1, 
    #                                             BATCH_SIZE)