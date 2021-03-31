import os,sys,inspect,subprocess

# this is a workaround to import test_helper which is in a parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir + '/../../')
sys.path.insert(0,parentdir) 
import test_helper

import toml
import sys

if __name__ == "__main__":
    """
        @function
            - expects a compiled contract with the correct batch size and that setup_merkle_proof was run.
            - sets up merkle proof test environment
            - executes cmd zkRelay merkle proof
        @parameters
            block_no = block number
            conf_file_path = config file with block data from blockchain

        exec.
        python3 compile_sm_merkle_proof.py <block_no> <batch_size> <conf_file_path>
        
    """
    if len(sys.argv) < 3:
        print('nope.')
        exit(1)

    block_no = int(sys.argv[1])
    batch_size = int(sys.argv[2])
    batch_no = int((block_no - ((block_no -1) % batch_size)) / batch_size) + 1
    conf_file_path = str(sys.argv[3])
    verbose = True

    ctx = test_helper.Context()
    ctx.obj = toml.load('./tests/conf/local_conf.toml')

    # rm output files from earlier tests
    verbose_output = subprocess.DEVNULL if verbose is False else None
    subprocess.run(['rm', 'mk_tree_validation/witness'], check=False, stdout=verbose_output)
    subprocess.run(['rm', 'mk_tree_validation/proof.json'], check=False, stdout=verbose_output)

    test_helper.exec_merkle_proof(ctx, 'test_smartContract/{}'.format(conf_file_path), block_no, verbose)