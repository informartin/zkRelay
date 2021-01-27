import json
import subprocess
import sys
import toml
from pytest_httpserver import HTTPServer
from preprocessing.create_input import generateZokratesInputFromBlock
from preprocessing.create_input import generateZokratesInputForMerkleProof
from zkRelay_cli import save_conf_file

general_zkRelayConf_file_path = './conf/zkRelay-cli.toml'
test_zkRelayConf_files_path = './tests/conf/local_conf.toml'

# Mock Click.Context object that is normally passed through cli to functions 
class Context:
    obj = {}

def setup_validate_test_environment(batch_size, batch_no, verbose=False):
    # rm output files from earlier tests
    verbose_output = subprocess.DEVNULL if verbose is False else None
    subprocess.run(['rm', 'output/witness{}'.format(batch_no)], check=False, stdout=verbose_output)
    subprocess.run(['rm', 'output/proof{}.json'.format(batch_no)], check=False, stdout=verbose_output)

    # normal conf has to be checked to see if the user did another batch size
    # before the first test
    current_setup_batch_size = check_zkRelay_setup_batch_size(batch_size)

    # check if correct files are already generated and zkRelay setup executed
    if current_setup_batch_size is not batch_size:
        print('\nSetting up validate test environment...')

        command = ['zkRelay', '-c', './tests/conf/local_conf.toml', 'generate-files', str(batch_size)]
        # output only if output is required
        if verbose is True: command.insert(1, '-v')
        subprocess.run(command,check=True,stdout=verbose_output)

        command = ['zkRelay', '-c', './tests/conf/local_conf.toml', 'setup']
        # output only if output is required
        if verbose is True: command.insert(1, '-v')
        subprocess.run(command,check=True,stdout=verbose_output)
        
        print('Done.')

def setup_merkle_proof_test_environment(batch_size, batch_no, verbose=False):
    print('\nSetting up merkle proof environment...')
    # rm output files from earlier tests
    verbose_output = subprocess.DEVNULL if verbose is False else None
    subprocess.run(['rm', 'mk_tree_validation/witness'], check=False, stdout=verbose_output)
    subprocess.run(['rm', 'mk_tree_validation/proof.json'], check=False, stdout=verbose_output)

    setup_validate_test_environment(batch_size, batch_no, verbose)

    subprocess.run(['zkRelay', 'setup-merkle-proof'],
                check=True, stdout=verbose_output)
    print('Done.')

"""
This function assumes that the cmd 'zkRelay validate' will execute 
the following function from the file 'preprocessing/zokrates_helper.py':

def validateBatchFromBlockNo(ctx, blockNo, batch_size):
    result = generateZokratesInputFromBlock(ctx, (blockNo-1)*batch_size+1, batch_size)
    os.system(cmd_compute_witness + result)
    os.system(cmd_generate_proof)
    os.system('mv witness output/witness' + str(blockNo))
    os.system('mv proof.json output/proof' + str(blockNo) + '.json')
"""
def exec_compute_witness(ctx, conf_file_path, batch_size, batch_no, verbose=False):
        host = ctx.obj.get('bitcoin_client').get('host')
        port = ctx.obj.get('bitcoin_client').get('port')
        verbose_output = subprocess.DEVNULL if verbose is False else None

        # get json config for test case
        fd = open(
            './tests/test_data/{}'.format(conf_file_path))
        config = json.load(fd)
        fd.close()

        try:
            with HTTPServer(host=host, port=port) as httpserver:
                # setup http server expected requests and responses
                request_count = len(config.get('http_responses'))
                for curr_request in range(request_count):
                    # TODO figure out how to overwrite request handler function
                    # expected_request_data = json.dumps(config.get('http_requests')[curr_request])\
                    #             if config.get('http_requests') is not None and not [] else None
                    expected_request_data = None
                    httpserver.expect_ordered_request(uri='/', data=expected_request_data)\
                                .respond_with_json(config.get('http_responses')[curr_request])

                # execute compute witness command from zokrates
                # SEE THE NOTE AT TOP OF THE FUNCITON FOR ASSUMPTIONS
                result = generateZokratesInputFromBlock(ctx, (batch_no-1)*batch_size+1, batch_size)
                try:
                    command_list = ('zokrates compute-witness --light -a ' + result).split(' ')
                    outcome = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    if (verbose): print(outcome.stdout.decode('utf-8'))
                    command_list = ('mv witness output/witness' + str(batch_no)).split(' ')
                    subprocess.run(command_list, stdout=verbose_output)
                    return outcome
                except subprocess.CalledProcessError:
                    return None
        except:
            print('There was probably a problem with the http server.')
            print(sys.exc_info())
            httpserver.check_assertions()

def exec_merkle_proof(ctx, conf_file_path, block_nr, verbose=False):
    host = ctx.obj.get('bitcoin_client').get('host')
    port = ctx.obj.get('bitcoin_client').get('port')
    verbose_output = subprocess.DEVNULL if not verbose else None

    # get json config for test case
    fd = open(
        './tests/test_data/{}'.format(conf_file_path))
    config = json.load(fd)
    fd.close()

    with HTTPServer(host=host, port=port) as httpserver:
        for http_response in config.get('http_responses'):
            httpserver.expect_ordered_request('/').respond_with_json(http_response)

        # SEE THE NOTE AT THE START OF THE FILE FOR ASSUMPTIONS
        #TODO make shell visible when verbose mode is on
        try:
            subprocess.run(['zkRelay', '-c', './tests/conf/local_conf.toml', 'create-merkle-proof', str(block_nr)],
                        check=True, stdout=verbose_output)
        except subprocess.CalledProcessError:
            return False

def exec_validate_cmd(ctx, conf_file_path, batch_no, verbose=False):
    host = ctx.obj.get('bitcoin_client').get('host')
    port = ctx.obj.get('bitcoin_client').get('port')
    verbose_output = subprocess.DEVNULL if not verbose else None

    # get json config for test case
    fd = open(
        './tests/test_data/{}'.format(conf_file_path))
    config = json.load(fd)
    fd.close()

    with HTTPServer(host=host, port=port) as httpserver:
        for http_response in config.get('http_responses'):
            httpserver.expect_ordered_request('/').respond_with_json(http_response)

        subprocess.run(['zkRelay', '-c', './tests/conf/local_conf.toml', 'validate', str(batch_no)], check=True, stdout=verbose_output)

def get_first_block_in_batch(batch_no, batch_size):
    return (batch_no - 1) * batch_size + 1

def check_zkRelay_setup_batch_size(batch_size):
    general_zkRelayConf = toml.load(general_zkRelayConf_file_path)
    test_zkRelayConf = toml.load(test_zkRelayConf_files_path)

    current_batch_size = general_zkRelayConf['zokrates_file_generator']['batch_size']

    if general_zkRelayConf['zokrates_file_generator']['batch_size'] is not batch_size:
        general_zkRelayConf['zokrates_file_generator']['batch_size'] = batch_size
        update_conf_file(general_zkRelayConf, general_zkRelayConf_file_path, batch_size)
    # elif might not be necessary...
    elif test_zkRelayConf['zokrates_file_generator']['batch_size'] is not batch_size:
        test_zkRelayConf['zokrates_file_generator']['batch_size'] = batch_size
        update_conf_file(general_zkRelayConf, general_zkRelayConf_file_path, batch_size)
    
    return current_batch_size

def update_conf_file(conf_obj, file_path, batch_size):
    # insert elements so that no error is thrown in save_conf_file
    conf_obj['general']['config_file_path'] = file_path
    conf_obj['general']['verbose_output'] = None
    conf_obj['general']['verbose'] = False
    
    ctx = Context()
    ctx.obj = conf_obj
    save_conf_file(ctx)