#!/usr/bin/env python
import sys
import os
from .create_input import generateZokratesInputFromBlock
from .create_input import generateZokratesInputForMerkleProof

cmd_echo = 'echo '
cmd_compute_witness = '| zokrates compute-witness --light --abi --stdin'
cmd_generate_proof = 'zokrates generate-proof'

#TODO change BlockNo to BatchNr
def validateBatchFromBlockNo(ctx, blockNo, batch_size):
    # result = generateZokratesInputFromBlock(ctx, (blockNo-1)*batch_size+1, batch_size) <- This was the previous implementation, however I don't understand how this should work
    result = generateZokratesInputFromBlock(ctx, blockNo, batch_size)
    os.system(cmd_echo + result + cmd_compute_witness)
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(blockNo))
    os.system('mv proof.json output/proof' + str(blockNo) + '.json')

def validateBatchesFromBlockNo(ctx, blockNo, amountBatches, batch_size):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(ctx, blockNo+i*batch_size, batch_size)
