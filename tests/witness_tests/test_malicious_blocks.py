import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer
import re
import subprocess
from preprocessing.create_input import generateZokratesInputFromBlock
from preprocessing.create_input import generateZokratesInputForMerkleProof

BATCH_SIZE = 2
BATCH_NO = 1

"""
The tests in this file assume that the cmd 'zkRelay validate' will execute 
the following function from the file 'preprocessing/zokrates_helper.py':

def validateBatchFromBlockNo(ctx, blockNo, batch_size):
    result = generateZokratesInputFromBlock(ctx, (blockNo-1)*batch_size+1, batch_size)
    os.system(cmd_compute_witness + result)
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(blockNo))
    os.system('mv proof.json output/proof' + str(blockNo) + '.json')
"""

# Mockup of Click.Context object that is normally passed through cli to functions
class Context:
    obj = {}
class TestMaliciousBlocks(unittest.TestCase):

    def setUp(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not BATCH_SIZE:
            print('Setting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(BATCH_SIZE),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')
        
        self.ctx = Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_malicious_block_hashes(self):
        """
            Valid return for getBlockHash
            Malicious return for first getBlock (
                    - wrong hash of first block in block sequence
        """
        self.exec_validate('malicious_block_hashes.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'malicious block hashes of blocks in batch were accepted')

    def test_malicious_merkle_roots(self):
        """
            Valid return for getBlockHash
            Malicious return for first getBlock 
                - wrong merkle root for block sequence
        """
        self.exec_validate('malicious_merkle_root.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'malicious merkle roots of blocks in batch were accepted')

    def test_malicious_prev_block(self):
        """
            returns valid getBlockHash
            malicious return for getBlock
                - malicious prev block hash
        """
        self.exec_validate('malicious_prev_block.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'malicious prevBlock was accepted')

    def test_malicious_epoch_block(self):
        """
            valid return for getBlockHash
            malicious return for getBlock
                - wrong block hash for epoch block
        """
        self.exec_validate('malicious_epoch_block.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'malicious epoch block was accepted')

    def test_wrong_but_valid_epoch_block(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block from another epoch
                - valid block sequence
        """
        self.exec_validate('wrong_but_valid_epoch_block.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid epoch block was accepted')

    def test_wrong_but_valid_blocks(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block
                - valid block sequence but not requested ones
        """
        self.exec_validate('wrong_but_valid_blocks.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid block sequence was accepted.')

    def test_wrong_but_valid_blocks_and_prevBlock(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block
                - valid block sequence but not requested ones
                - valid prevBlock to block sequence
        """
        self.exec_validate('wrong_but_valid_blocks_and_prevBlock.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid block sequence and prevBlock were accepted.')

    def test_wrong_but_valid_blocks_other_epoch(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block
                - valid block sequence from another epoch
        """
        self.exec_validate('wrong_but_valid_blocks_other_epoch.json')

        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid block batch from other epoch was accepted.')

    def test_wrong_but_valid_epoch_block_and_blocks(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block from another epoch
                - valid block sequence from same epoch as epoch_block
                - valid prev block
        """
        self.exec_validate('wrong_but_valid_epoch_block_and_blocks.json')
        
        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid epoch block and block sequence were accepted')

    def test_wrong_but_valid_epoch_block_and_blocks_and_prevBlock(self):
        """
            returns valid getBlockHash
            malicious return for getBlock 
                - valid epoch_block from another epoch
                - valid block sequence from other epoch as epoch_block
                - valid prevBlock to block sequence
        """
        self.exec_validate('wrong_but_valid_epoch_block_and_blocks_and_prevBlock.json')

        # checking if output found error with help of regex
        with open('./output/witness1', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 0$', lines[6])
            self.assertIsNotNone(check, 'wrong but valid epoch block, block sequence and prevBlock were accepted')

    def exec_validate(self, http_conf_file):
        host = self.ctx.obj.get('bitcoin_client').get('host')
        port = self.ctx.obj.get('bitcoin_client').get('port')

        # get json config for test case
        fd = open(
            './tests/test_data/test_witness/test_malicious_blocks/{}'.format(http_conf_file))
        config = json.load(fd)
        fd.close()

        with HTTPServer(host=host, port=port) as httpserver:
            for http_response in config.get('http_responses'):
                httpserver.expect_ordered_request('/').respond_with_json(http_response)

            # SEE THE NOTE AT THE START OF THE FILE FOR ASSUMPTIONS
            #TODO make shell visible when verbose mode is on
            result = generateZokratesInputFromBlock(self.ctx, (BATCH_NO-1)*BATCH_SIZE+1, BATCH_SIZE)
            command_list = ('zokrates compute-witness --light -a ' + result).split(' ')
            try:
                subprocess.run(command_list,
                            check=True, shell=False)
                command_list = ('mv witness output/witness' + str(BATCH_NO)).split(' ')
                subprocess.run(command_list,
                            check=True, shell=False)
            except subprocess.CalledProcessError:
                return False
            

if __name__ == "__main__":
    unittest.main()