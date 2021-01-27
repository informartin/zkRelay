import unittest
import toml
import json
import preprocessing
from pytest_httpserver import HTTPServer
import re
import subprocess
from preprocessing.create_input import generateZokratesInputFromBlock
from preprocessing.create_input import generateZokratesInputForMerkleProof
import sys
from tests import test_helper

class TestWitnessCorrectBlocks(unittest.TestCase):
    conf_dir_path = 'test_witness/test_correct_blocks/'
    verbose = True

    def setUp(self):
        self.ctx = test_helper.Context()
        self.ctx.obj = toml.load('./tests/conf/local_conf.toml')

    def test_1_start_of_epoch(self):
        batch_size = 2
        batch_no = 1

        # check if required files are generated
        test_helper.setup_validate_test_environment(batch_size, batch_no, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}start_of_epoch.json'.format(self.conf_dir_path), batch_size, batch_no, self.verbose)
        
        check = re.search('Witness:', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, '{} blocks at start of epoch werent processed correctly.'.format(batch_size))

    def test_2_end_of_epoch(self):
        batch_size = 5
        batch_no = 403

        # check if required files are generated
        test_helper.setup_validate_test_environment(batch_size, batch_no, verbose=self.verbose)

        result = test_helper.exec_compute_witness(self.ctx, '{}end_of_epoch.json'.format(self.conf_dir_path), batch_size, batch_no, verbose=self.verbose)
        
        check = re.search('Witness:', result.stdout.decode('utf-8'))
        self.assertIsNotNone(check, '{} blocks right at end of epoch werent processed correctly.'.format(batch_size))