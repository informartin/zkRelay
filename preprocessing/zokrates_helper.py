#!/usr/bin/env python
import sys
import os
from .create_input import generateZokratesInputFromBlock
from .create_input import generateZokratesInputForMerkleProof

cmd_compute_witness = 'zokrates compute-witness --light -a '
cmd_generate_proof = 'zokrates generate-proof'

def validateBatchFromBlockNo(blockNo, batch_size):
    os.system(cmd_compute_witness + generateZokratesInputFromBlock((blockNo-1)*batch_size+1, batch_size))
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(blockNo))
    os.system('mv proof.json output/proof' + str(blockNo) + '.json')

def validateBatchesFromBlockNo(blockNo, amountBatches, batch_size):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(blockNo+i*batch_size, batch_size)