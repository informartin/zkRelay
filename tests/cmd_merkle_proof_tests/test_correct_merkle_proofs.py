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

class TestCorrectMerkleProofs(unittest.TestCase):
    verbose = True

    def setUp(self):
        self.ctx = test_helper.Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_batch_size_2(self):
        """
            testing all blocks of batch size 2
        """
        batch_size = 2
        batch_no = 1
        first_block_in_batch = test_helper.get_first_block_in_batch(batch_no, batch_size)
        block_range = test_helper.get_first_block_in_batch(batch_no + 1, batch_size)

        # check if required files are generated 
        test_helper.setup_merkle_proof_test_environment(batch_size, batch_no, self.verbose)

        for block_nr in range(first_block_in_batch, block_range):
            counter = (block_nr - 1) % batch_size
            
            test_helper.exec_merkle_proof(self.ctx, 'test_proof/test_correct_proofs/batch_size_2_nr_{}.json'.format(counter), block_nr, self.verbose)
            
            with open('./mk_tree_validation/witness', 'r') as witness:
                lines = witness.readlines()

                self.assertEqual(lines[0].rstrip(), '~out_3 293162789692691517568381246587735157467', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
                
                self.assertEqual(lines[1].rstrip(), '~out_2 11010401775869175601781796382403673205', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))

    def test_batch_size_5(self):
        """
            testing all blocks of batch size 5
        """
        batch_size = 5
        batch_no = 1
        first_block_in_batch = test_helper.get_first_block_in_batch(batch_no, batch_size)
        block_range = test_helper.get_first_block_in_batch(batch_no + 1, batch_size)

        # check if required files are generated 
        test_helper.setup_merkle_proof_test_environment(batch_size, batch_no, self.verbose)

        for block_nr in range(first_block_in_batch, block_range):
            counter = (block_nr - 1) % batch_size
            
            test_helper.exec_merkle_proof(self.ctx, 'test_proof/test_correct_proofs/batch_size_5_nr_{}.json'.format(counter), block_nr, verbose=self.verbose)
            
            with open('./mk_tree_validation/witness', 'r') as witness:
                lines = witness.readlines()

                self.assertEqual(lines[0].rstrip(), '~out_3 31499779437727666674347312136552582663', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
                
                self.assertEqual(lines[1].rstrip(), '~out_2 30029047865384282741416230607321619582', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))

    def test_batch_size_10(self):
        """
            testing all blocks of batch size 10
        """
        batch_size = 10
        batch_no = 1
        first_block_in_batch = test_helper.get_first_block_in_batch(batch_no, batch_size)
        block_range = test_helper.get_first_block_in_batch(batch_no + 1, batch_size)

        # check if required files are generated 
        test_helper.setup_merkle_proof_test_environment(batch_size, batch_no, self.verbose)

        for block_nr in range(first_block_in_batch, block_range):
            counter = (block_nr - 1) % batch_size
            
            test_helper.exec_merkle_proof(self.ctx, 'test_proof/test_correct_proofs/batch_size_10_nr_{}.json'.format(counter), block_nr, self.verbose)
            
            with open('./mk_tree_validation/witness', 'r') as witness:
                lines = witness.readlines()

                self.assertEqual(lines[0].rstrip(), '~out_3 16337350273637649591439682102568762216', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
                
                self.assertEqual(lines[1].rstrip(), '~out_2 11202167189876744263973656195464312346', 
                        'inclusion prove for block nr {} in merkle tree of {} blocks was not successful.'.format(block_nr, batch_size))
