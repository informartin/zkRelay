#!/usr/bin/env python
import sys
import os
from create_input import generateZokratesInputFromBlock

cmd_compute_witness = 'zokrates compute-witness --light -a '
cmd_generate_proof = 'zokrates generate-proof'


for i in range(20,21):
    os.system(cmd_compute_witness + generateZokratesInputFromBlock((i-1)*504+1, 504))
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(i))
    os.system('mv proof.json output/proof' + str(i) + '.json')
