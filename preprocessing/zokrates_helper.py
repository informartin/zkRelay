#!/usr/bin/env python
import sys
import subprocess
from .create_input import generateZokratesInputFromBlock
from .create_input import generateZokratesInputForMerkleProof
from colorama import init as initColor
from termcolor import colored 

initColor()

cmd_compute_witness = 'zokrates compute-witness --light -a '
cmd_generate_proof = 'zokrates generate-proof'

def validateBatchFromBlockNo(ctx, batch_no, batch_size, verbose_output=subprocess.DEVNULL):
    print(colored('Getting block information and generating zokrates input...', 'cyan'))
    result = generateZokratesInputFromBlock(ctx, (batch_no-1)*batch_size+1, batch_size)
    print(colored('Done!', 'green'))

    print(colored('Exec "{}"'.format(cmd_compute_witness), 'cyan'))
    command = ['/usr/bin/time', '-f', 'Max used memory during exec: %M kbytes']
    command += cmd_compute_witness.split() + result.split()
    subprocess.run(command, check=True, stdout=verbose_output)
    print(colored('Done!', 'green'))

    print(colored('Exec "{}"'.format(cmd_generate_proof), 'cyan'))
    command = ['/usr/bin/time', '-f', 'Max used memory during exec: %M kbytes']
    command += cmd_generate_proof.split()
    subprocess.run(command, check=True, stdout=verbose_output)
    print(colored('Done!', 'green'))

    command = ['mv', 'witness'] + ['output/witness{}'.format(batch_no)]
    print(colored('Exec "{}"'.format(' '.join(command)), 'cyan'))
    subprocess.run(command, check=True, stdout=verbose_output)
    print(colored('Done!', 'green'))

    command = ['mv', 'proof.json'] + ['output/proof{}.json'.format(batch_no)]
    print(colored('Exec "{}"'.format(' '.join(command)), 'cyan'))
    subprocess.run(command, check=True, stdout=verbose_output)
    print(colored('Done!', 'green'))

def validateBatchesFromBlockNo(ctx, batch_no, amountBatches, batch_size, verbose_output=subprocess.DEVNULL):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(ctx, batch_no+i*batch_size, batch_size)