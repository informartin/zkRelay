#!/usr/bin/env python
import sys
import os
from .create_input import generateZokratesInputFromBlock
from .create_input import generateZokratesInputForMerkleProof

cmd_compute_witness = 'zokrates compute-witness --light -a '
cmd_generate_proof = 'zokrates generate-proof'

def validateBatchFromBlockNo(ctx, batchNr, batch_size):
    result = generateZokratesInputFromBlock(ctx, (batchNr-1)*batch_size+1, batch_size)
    os.system(cmd_compute_witness + result)
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(batchNr))
    os.system('mv proof.json output/proof' + str(batchNr) + '.json')

def validateBatchesFromBlockNo(ctx, batchNr, amountBatches, batch_size):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(ctx, batchNr+i*batch_size, batch_size)