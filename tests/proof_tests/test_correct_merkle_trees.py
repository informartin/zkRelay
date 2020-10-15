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

        print('\nSetting up merkle proof environment...\n')
        subprocess.run(['zkRelay', 'setup-merkle-proof'],
                    check=True, stdout=subprocess.DEVNULL)
        print('\nDone.')

    def test_batch_size_2(self):
        """
            testing all blocks of batch size 2
        """
        batch_size = 2
        batch_no = 1
        first_block_in_batch = test_helper.get_first_block_in_batch(batch_no, batch_size)

        # check if required files are generated 
        test_helper.setup_test_environment(batch_size, batch_no)

        for block_nr in range(first_block_in_batch, (batch_no * batch_size) + 1):
            counter = (block_nr - 1) % batch_size
            
            test_helper.exec_proof(self.ctx, '/test_proof/test_correct_proofs/batch_size_2_nr_{}.json'.format(counter), block_nr)
            
            with open('./mk_tree_validation/witness', 'r') as witness:
                lines = witness.readlines()

                self.assertEqual(lines[0].rstrip(), '~out_3 293162789692691517568381246587735157467', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
                
                self.assertEqual(lines[1].rstrip(), '~out_2 11010401775869175601781796382403673205', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
