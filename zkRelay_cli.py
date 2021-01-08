#!/usr/bin/env python
import os
import sys
import subprocess
import click
import copy
import re
import generate_zokrates_files as zokrates_file_generator
import preprocessing
import toml
from colorama import init as initColor
from termcolor import colored 

initColor()

SUPPORTED_VERSION_ZOKRATES = '0.5.1'
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--no-verbose',
                is_flag=True,
                help='disable verbose output')
@click.option('-c',
                '--config-file',
                help='path to config file',
                required=False,
                type=click.STRING)
@click.pass_context
def zkRelay_cli(ctx, no_verbose, config_file):
    """
    For more information about a command
    use 'cli COMMAND [-h, --help]'
    """
    # check if correct zokrates version is used. (currently supported 0.5.1)
    result = subprocess.run(['zokrates', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode is not 0:
        print(colored('Was not able to execute zokrates.', 'red') + ' Did you install it? (currently supported version = {})'.format(SUPPORTED_VERSION_ZOKRATES))
        exit(-1)
    correct_version = re.search('.*{}'.format(SUPPORTED_VERSION_ZOKRATES), result.stdout.decode("utf-8"))
    if correct_version is None:
        curr_version = re.search('(\d+((\.\d+)?(\.\d+)?))', result.stdout.decode('utf-8'))
        print(colored('Unsupported version of zokrates.({})'.format(curr_version.group(0)), 'red') + 'Currently supported: {}'.format(SUPPORTED_VERSION_ZOKRATES))
        exit(-1)

    # load conf file to pass to cmds
    config_file_path = config_file if config_file is not None else './conf/zkRelay-cli.toml'
    ctx.obj = toml.load(config_file_path)
    ctx.obj['general']['config_file_path'] = config_file_path

    # check if verbose output is required
    if no_verbose:
        ctx.obj['general']['verbose_output'] = subprocess.DEVNULL
        ctx.obj['general']['verbose'] = False
    else:
        ctx.obj['general']['verbose_output'] = None
        ctx.obj['general']['verbose'] = True
        

@zkRelay_cli.command('generate-files')
@click.argument('batch_size',
                required=True,
                type=click.INT)
@click.pass_context
def generate_files(ctx, batch_size):
    click.echo(colored('Generating...', 'cyan'))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_validation_code(batch_size), "validate.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_root_code(batch_size), "compute_merkle_root.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_merkle_proof_validation_code(batch_size), "verify_merkle_proof.zok".format(i=batch_size))
    
    if not os.path.exists('mk_tree_validation'):
        os.mkdir('mk_tree_validation')
    os.rename("verify_merkle_proof.zok", "mk_tree_validation/verify_merkle_proof.zok")
    click.echo(colored('Done.', 'green'))

    # save batch_size in smart contract batch_verifier.sol
    click.echo(colored('Updating batch_verifier.sol...', 'cyan'))
    with open('batch_verifier.sol', 'r') as r_batch_verifier_file:
        # get content of smart contract and replace batch_size
        old_contract_content = r_batch_verifier_file.read()
        new_contract_content = re.sub('BATCH_SIZE = \d+', 'BATCH_SIZE = {}'.format(batch_size), old_contract_content)
        
        # save new content with updated batch_size
        with open('batch_verifier.sol', 'w') as w_batch_verifier_file:
            w_batch_verifier_file.write(new_contract_content)
    click.echo(colored('Done.', 'green'))

    # save batch_size in conf file for later use
    ctx.obj['zokrates_file_generator']['batch_size'] = batch_size
    save_conf_file(ctx)

@zkRelay_cli.command()
@click.option('-m', '--multiple_batches',
                required=False,
                help='Nr. of how many batches',
                type=click.INT)
@click.option('-bch', '--bc-host',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.option('-bcp', '--bc-port',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.INT)
@click.option('-bcu', '--bc-user',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.option('-bcpw', '--bc-pwd',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.argument('batch_no',
                type=click.INT)
@click.pass_context
def validate(ctx, batch_no, multiple_batches, bc_host, bc_port, bc_user, bc_pwd):
    batch_size = int(ctx.obj['zokrates_file_generator']['batch_size'])
    verbose_output = ctx.obj['general']['verbose_output']

    try:
        ctx = processBCClientConf(ctx, bc_host, bc_port, bc_user, bc_pwd)
    except:
        click.echo(colored('Error, cannot validate.', 'red'))
        click.echo(colored('Missing argument: ', 'red') + 'bc-host, bc-port, bc-user or bc-pwd not set in config file located at {}.'.format(ctx.obj['general']['config_file_path']))
        return

    if multiple_batches is not None:
        preprocessing.validateBatchesFromBlockNo(ctx,
                                                    batch_no,
                                                    multiple_batches, 
                                                    batch_size,
                                                    verbose_output)
    else:
        preprocessing.validateBatchFromBlockNo(ctx,
                                                batch_no, 
                                                batch_size,
                                                verbose_output)

@zkRelay_cli.command()
@click.option('-bch', '--bc-host',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.option('-bcp', '--bc-port',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.INT)
@click.option('-bcu', '--bc-user',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.option('-bcpw', '--bc-pwd',
                required=False,
                show_default='See conf/zkRelay-cli.toml', 
                type=click.STRING)
@click.argument('block_no',
                type=click.INT)
@click.pass_context
def create_merkle_proof(ctx, block_no, bc_host, bc_port, bc_user, bc_pwd):
    verbose_output = ctx.obj['general']['verbose_output']
    batch_size = int(ctx.obj['zokrates_file_generator']['batch_size'])

    try:
        ctx = processBCClientConf(ctx, bc_host, bc_port, bc_user, bc_pwd)
    except:
        click.echo(colored('Error, cannot validate.', 'red'))
        click.echo(colored('Missing argument: ', 'red') + 'bc-host, bc-port, bc-user or bc-pwd not set in config file located at {}.'.format(ctx.obj['general']['config_file_path']))
        return
    click.echo(colored('Getting block information and generating zokrates input...', 'cyan'))
    first_block_in_batch = block_no - ((block_no -1) % batch_size)
    block_hashes = [preprocessing.littleEndian(header) for header in preprocessing.getBlockHeadersInRange(ctx, first_block_in_batch, first_block_in_batch + batch_size)]
    target_header_hash = block_hashes[(block_no - 1) % batch_size]
    tree = preprocessing.compute_full_merkle_tree(block_hashes)
    header = preprocessing.createZokratesInputFromBlock(preprocessing.getBlocksInRange(ctx, block_no, block_no+1)[0])
    zokrates_input = preprocessing.get_proof_input(tree, target_header_hash, header)
    print(colored('Done!', 'green'))

    try:
        click.echo(colored('Exec "zokrates compute-witness --light"', 'cyan'))
        command = ['zokrates', 'compute-witness', '--light', '-a']
        command += zokrates_input.split(' ')
        subprocess.run(command, check=True, cwd="mk_tree_validation/", stdout=verbose_output)
        click.echo(colored('Done!', 'green'))

        click.echo(colored('Exec "zokrates generate-proof"', 'cyan'))
        subprocess.run(['zokrates', 'generate-proof'], stdout=verbose_output,
                        check=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
    except subprocess.CalledProcessError:
        click.echo('Error while computing merkle treeinclusion proof')
        click.echo(sys.exc_info()[0])

@zkRelay_cli.command(short_help='Generates proof validator')
@click.pass_context
def setup(ctx):
    """
    Executes 3 cmds:

    1. compile validation program

    2. generate verification keys

    3. generate smart contract that validates proofs
    """
    verbose_output = ctx.obj['general']['verbose_output']

    try:
        click.echo(colored('Exec "zokrates compile --light -i validate.zok"', 'cyan'))
        subprocess.run(['zokrates', 'compile', '--light', '-i', 'validate.zok'], stdout=verbose_output,
                        check=True)
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates setup --light"', 'cyan'))
        subprocess.run(['zokrates', 'setup', '--light'], stdout=verbose_output,
                        check=True)
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates export-verifier"', 'cyan'))
        subprocess.run(['zokrates', 'export-verifier'], stdout=verbose_output,
                        check=True)
        click.echo(colored('Done!', 'green'))
    except subprocess.CalledProcessError:
        click.echo('Error while generating proof validator')
        click.echo(sys.exc_info()[0])

@zkRelay_cli.command(short_help='Generates merkle proof validator')
@click.pass_context
def setup_merkle_proof(ctx):
    verbose_output = ctx.obj['general']['verbose_output']

    try:
        click.echo(colored('Exec "zokrates compile --light -i verify_merkle_proof.zok"', 'cyan'))
        subprocess.run(['zokrates', 'compile', '--light', '-i', 'verify_merkle_proof.zok'], stdout=verbose_output,
                        check=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates setup --light"', 'cyan'))
        subprocess.run(['zokrates', 'setup', '--light'], stdout=verbose_output,
                        check=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates export-verifier"', 'cyan'))
        subprocess.run(['zokrates', 'export-verifier'], stdout=verbose_output,
                        check=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
    except subprocess.CalledProcessError:
        click.echo('Error while generating merkle proof validator')
        click.echo(sys.exc_info()[0])    


def processBCClientConf(ctx, bc_host, bc_port, bc_user, bc_pwd):
    # override defaults in conf file with parameters from command line
    if bc_host is not None: ctx.obj['bitcoin_client']['host'] = bc_host
    if bc_port is not None: ctx.obj['bitcoin_client']['port'] = bc_port
    if bc_user is not None: ctx.obj['bitcoin_client']['user'] = bc_user
    if bc_pwd is not None: ctx.obj['bitcoin_client']['pwd'] = bc_pwd
    
    # check if any values where omitted
    if ctx.obj['bitcoin_client']['host'] is None:
        raise Exception
    if ctx.obj['bitcoin_client']['port'] is None:
        raise Exception
    if ctx.obj['bitcoin_client']['user'] is None:
        raise Exception
    if ctx.obj['bitcoin_client']['pwd'] is None:
        raise Exception
    return ctx

def save_conf_file(ctx):
    click.echo(colored('Updating conf file...', 'cyan'))

    with open(ctx.obj['general']['config_file_path'], 'w') as fd:
        # deleting unnecessary entries
        conf = copy.deepcopy(ctx.obj)
        del conf['general']['config_file_path']
        del conf['general']['verbose_output']
        del conf['general']['verbose']
        toml.dump(conf, fd)

    click.echo(colored('Done!', 'green'))