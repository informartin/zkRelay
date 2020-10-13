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
from tests import test_helper


BATCH_SIZE=2

# Mock Click.Context object that is normally passed through cli to functions 
class Context:
    obj = {}

class TestProofCorrectBlocks(unittest.TestCase):

    def setUp(self):
        self.ctx = Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

        # check if 'zkRelay setup-merkle-proof' was executed already
        print('\nSetting up merkle proof environment...\n')
        subprocess.run(['zkRelay', 'setup-merkle-proof'],
                    check=True, stdout=subprocess.DEVNULL)
        print('\nDone.')

    def test_1_start_of_epoch(self):
        # check if required files are generated 
        batch_size = 2
        batch_no = 1
        block_nr = 1
        test_helper.setup_test_environment(batch_size, batch_no)

        test_helper.exec_proof(self.ctx, '/test_proof/test_correct_proof/start_of_epoch.json', block_nr)
        
        with open('./mk_tree_validation/witness', 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, 'inclusion prove for block nr {} in merkle tree of {} blocks at start of epoch was not successful.'.format(block_nr, batch_size))

    def test_2_middle_of_epoch(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 5:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(5),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        test_helper.exec_proof(self.ctx, '5_blocks.json', block_nr=3)
        
        with open('./output/witness{}'.format(5), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, 'inclusion prove for block nr 3 in merkle tree of 5 blocks was not successful.')

    def test_3_end_of_epoch(self):
        # check if required files are generated 
        zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
        if zkRelayConf['zokrates_file_generator']['batch_size'] is not 5:
            print('\nSetting up test environment...\n')
            subprocess.run('zkRelay generate-files {}'.format(5),
                        check=True, shell=True)
            subprocess.run('zkRelay setup',
                        check=True, shell=True)
            print('\nDone.')

        test_helper.exec_proof('5_blocks.json', block_nr=3)
        
        with open('./output/witness{}'.format(5), 'r') as witness:
            lines = witness.readlines()
            check = re.match('^~out_0 1$', lines[6])
            self.assertIsNotNone(check, 'inclusion prove for block nr 3 in merkle tree of 5 blocks was not successful.')


    # def test_20_blocks(self):
    #     # check if required files are generated 
    #     zkRelayConf = toml.load('./conf/zkRelay-cli.toml')
    #     if zkRelayConf['zokrates_file_generator']['batch_size'] is not 20:
    #         print('\nSetting up test environment...\n')
    #         subprocess.run('zkRelay generate-files {}'.format(20),
    #                     check=True, shell=True)
    #         subprocess.run('zkRelay setup',
    #                     check=True, shell=True)
    #         print('\nDone.')

    #     self.exec_proof('20_blocks.json', block_nr=9)
        
    #     with open('./output/witness{}'.format(1), 'r') as witness:
    #         lines = witness.readlines()
    #         check = re.match('^~out_0 1$', lines[6])
    #         self.assertIsNotNone(check, '20 blocks werent processed.')
