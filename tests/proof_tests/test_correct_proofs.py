import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer
import re
import subprocess
from preprocessing.create_input import generateZokratesInputFromBlock
from preprocessing.create_input import generateZokratesInputForMerkleProof
import os


BATCH_SIZE=2

# Mock Click.Context object that is normally passed through cli to functions 
class Context:
    obj = {}

class TestProofCorrectBlocks(unittest.TestCase):

    def setUp(self):
        self.ctx = Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

        # check if 'zkRelay setup-merkle-proof' was executed already
        if os.path.isfile('./mk_tree_validation/proving.key') is False:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay setup-merkle-proof',
                        check=True, shell=True)
            print('\nDone.')

    def test_5_blocks(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 5:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(5),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        self.exec_proof('5_blocks.json', block_nr=3)
        
        with open('./output/witness{}'.format(1), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, 'inclusion prove for block nr 3 in merkle tree of 5 blocks was not successful.')


    def test_20_blocks(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 20:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(20),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        self.exec_proof('20_blocks.json', block_nr=9)
        
        with open('./output/witness{}'.format(1), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, '20 blocks werent processed.')

    def exec_proof(self, http_conf_file, block_nr):
        host = self.ctx.obj.get('bitcoin_client').get('host')
        port = self.ctx.obj.get('bitcoin_client').get('port')

        # get json config for test case
        fd = open(
            './tests/test_data/test_proof/test_correct_proofs/{}'.format(http_conf_file))
        config = json.load(fd)
        fd.close()

        with HTTPServer(host=host, port=port) as httpserver:
            for http_response in config.get('http_responses'):
                httpserver.expect_ordered_request('/').respond_with_json(http_response)

            # SEE THE NOTE AT THE START OF THE FILE FOR ASSUMPTIONS
            #TODO make shell visible when verbose mode is on
            try:
                subprocess.run('zkRelay create-merkle-proof {}'.format(block_nr),
                            check=True, shell=False)
            except subprocess.CalledProcessError:
                return False
