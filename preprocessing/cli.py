#!/usr/bin/env python
import sys
import os
from create_input import generateZokratesInputFromBlock
from create_input import generateZokratesInputForMerkleProof

cmd_compute_witness = 'zokrates compute-witness --light -a '
cmd_generate_proof = 'zokrates generate-proof'
BATCH_SIZE = 21

def validateBatchFromBlockNo(blockNo):
    os.system(cmd_compute_witness + generateZokratesInputFromBlock((blockNo-1)*BATCH_SIZE+1, BATCH_SIZE))
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(blockNo))
    os.system('mv proof.json output/proof' + str(blockNo) + '.json')

def validateBatchesFromBlockNo(blockNo, amountBatches):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(blockNo+i*BATCH_SIZE)

def main():
    arguments = len(sys.argv) - 1

    if sys.argv[1] == "validate_blocks":
        if arguments == 2:
            validateBatchFromBlockNo(int(sys.argv[2]))
        if arguments == 3:
            validateBatchesFromBlockNo(int(sys.argv[2]),int(sys.argv[3]))
    elif sys.argv[1] == "create_input_merkle_root":
        print(generateZokratesInputForMerkleProof(int(sys.argv[2]), BATCH_SIZE))


if __name__ == "__main__":
    main()
