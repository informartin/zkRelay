import os,sys,inspect

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
            - generates contract files according to batch_size
            - sets up validate test environment
            - executes cmd zkRelay validate
        @parameters
            batch_size = batch size
            batch_no = batch number
            conf_file_path = config file with block data from blockchain

        exec.
        python3 compile_SM_validate_batch.py <batch_size> <batch_no> <conf_file_path>
        
    """
    if len(sys.argv) < 4:
        print('nope.')
        exit(1)

    batch_size = int(sys.argv[1])
    batch_no = int(sys.argv[2])
    conf_file_path = str(sys.argv[3])
    verbose = True

    ctx = test_helper.Context()
    ctx.obj = toml.load('./tests/conf/local_conf.toml')

    test_helper.setup_validate_test_environment(batch_size, batch_no, verbose)

    test_helper.exec_validate_cmd(ctx, 'test_smartContract/{}'.format(conf_file_path), batch_no, verbose)