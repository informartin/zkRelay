import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer
import re
import subprocess
from tests import test_helper

BATCH_SIZE = 2
BATCH_NO = 1

class TestMaliciousBlocks(unittest.TestCase):
    conf_dir_path = 'test_witness/test_malicious_blocks/'
    verbose = True

    def setUp(self):        
        self.ctx = test_helper.Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_1_malicious_merkle_roots(self):
        """
            Valid return for getBlockHash
            Malicious return for first getBlock 
                - wrong merkle root for block sequence
        """
        # check if required files are generated
        test_helper.setup_validate_test_environment(BATCH_SIZE, BATCH_NO, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}malicious_merkle_root.json'.format(self.conf_dir_path), BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        # checking if output found error with help of regex
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, 'malicious merkle roots of blocks in batch were accepted')

    def test_2_malicious_blocks_version_hex(self):
        """
            Valid return for getBlockHash
            Malicious return for first getBlock 
                - wrong merkle root for block sequence
        """
        # check if required files are generated 
        test_helper.setup_validate_test_environment(BATCH_SIZE, BATCH_NO, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}malicious_blocks_version_hex.json'.format(self.conf_dir_path), BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        # checking if output found error with help of regex
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, 'malicious version hex of blocks in batch were accepted')

    def test_3_malicious_prev_block(self):
        """
            returns valid getBlockHash
            malicious return for getBlock
                - malicious prev block hash
        """
        # check if required files are generated 
        test_helper.setup_validate_test_environment(BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        result = test_helper.exec_compute_witness(self.ctx, '{}malicious_prev_block.json'.format(self.conf_dir_path), BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        # checking if output found error with help of regex
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, 'malicious prevBlock was accepted')

    def test_5_epoch_block_non_sufficient_pow(self):
        """
            testing epoch block with non_sufficient_pow
        """
        # check if required files are generated 
        test_helper.setup_validate_test_environment(BATCH_SIZE, BATCH_NO, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}epoch_block_non_sufficient_pow.json'.format(self.conf_dir_path), BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        # checking if output found error with help of regex
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, 'non sufficient pow of epoch block was accepted')

    def test_6_block_batch_non_sufficient_pow(self):
        """
            testing block batch with non_sufficient_pow
        """
        # check if required files are generated 
        test_helper.setup_validate_test_environment(BATCH_SIZE, BATCH_NO, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}block_batch_non_sufficient_pow.json'.format(self.conf_dir_path), BATCH_SIZE, BATCH_NO, verbose=self.verbose)
        
        # checking if output found error with help of regex
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, 'non sufficient pow of block batch was accepted')

    def test_7_crossover_of_epochs(self):
        """
            testing block batch that overlaps an epoch
        """
        batch_size = 5
        batch_no = 99994

        # check if required files are generated 
        test_helper.setup_validate_test_environment(batch_size, batch_no, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}crossover_of_epochs.json'.format(self.conf_dir_path), batch_size, batch_no, verbose=self.verbose)
        
        check = re.search('Execution failed', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, '{} blocks at a crossover between epochs were processed.'.format(batch_size))
            

if __name__ == "__main__":
    unittest.main()