import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer
import re
import subprocess
from preprocessing.create_input import generateZokratesInputFromBlock
from preprocessing.create_input import generateZokratesInputForMerkleProof


BATCH_SIZE=2

# Mock Click.Context object that is normally passed through cli to functions 
class Context:
    obj = {}

class TestWitnessCorrectBlocks(unittest.TestCase):

    def setUp(self):
        self.ctx = Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_2_blocks(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 2:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(2),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        self.exec_validate('2_blocks.json', batch_size=2, batch_no=1)
        
        with open('./output/witness{}'.format(1), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, '2 blocks werent processed.')


    def test_30_blocks(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 20:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(20),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        self.exec_validate('20_blocks.json', batch_size=20, batch_no=1)
        
        with open('./output/witness{}'.format(1), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, '20 blocks werent processed.')

    def exec_validate(self, http_conf_file, batch_size, batch_no):
        host = self.ctx.obj.get('bitcoin_client').get('host')
        port = self.ctx.obj.get('bitcoin_client').get('port')

        # get json config for test case
        fd = open(
            './tests/test_data/test_witness/test_correct_blocks/{}'.format(http_conf_file))
        config = json.load(fd)
        fd.close()

        with HTTPServer(host=host, port=port) as httpserver:
            for http_response in config.get('http_responses'):
                httpserver.expect_ordered_request('/').respond_with_json(http_response)

            # SEE THE NOTE AT THE START OF THE FILE FOR ASSUMPTIONS
            #TODO make shell visible when verbose mode is on
            result = generateZokratesInputFromBlock(self.ctx, (batch_no-1)*batch_size+1, batch_size)
            command_list = ('zokrates compute-witness --light -a ' + result).split(' ')
            try:
                subprocess.run(command_list,
                            check=True, shell=False)
                command_list = ('mv witness output/witness' + str(batch_no)).split(' ')
                subprocess.run(command_list,
                            check=True, shell=False)
            except subprocess.CalledProcessError:
                return False

    # def test_correct_blocks_online(self):
    #     self.ctx.obj = toml.load('./tests/conf/online_conf.toml')

    #     preprocessing.validateBatchFromBlockNo(self.ctx,
    #                                             1, 
    #                                             BATCH_SIZE)