#!/usr/bin/env python
import os
import sys
import subprocess
import click
import generate_zokrates_files as zokrates_file_generator
import preprocessing
import toml
from colorama import init as initColor
from termcolor import colored 

initColor()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def zkRelay_cli(ctx):
    """
    For more information about a command
    use 'cli COMMAND [-h, --help]'
    """
    # load conf file to pass to cmds
    ctx.obj = toml.load('./conf/zkRelay-cli.toml')
    pass

@zkRelay_cli.command('generate-files')
@click.argument('batch_size',
                required=True,
                type=click.INT)
@click.pass_context
def generate_files(ctx, batch_size):
    click.echo('Generating...')
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_validation_code(batch_size), "validate.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_root_code(batch_size), "compute_merkle_root.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_merkle_proof_validation_code(batch_size), "verify_merkle_proof.zok".format(i=batch_size))
    if not os.path.exists('mk_tree_validation'):
        os.mkdir('mk_tree_validation')
    os.rename("verify_merkle_proof.zok", "mk_tree_validation/verify_merkle_proof.zok")
    click.echo('Done.')
    # save batch_size in conf file for later use
    click.echo('Updating conf file...')
    ctx.obj['zokrates_file_generator']['batch_size'] = batch_size
    fd = open('./conf/zkRelay-cli.toml', 'w')
    toml.dump(ctx.obj, fd)
    click.echo('Done.')

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
@click.argument('first_block_in_batch',
                type=click.INT)
@click.pass_context
def validate(ctx, first_block_in_batch, multiple_batches, bc_host, bc_port, bc_user, bc_pwd):
    batch_size = int(ctx.obj['zokrates_file_generator']['batch_size'])

    try:
        ctx = processBCClientConf(ctx, bc_host, bc_port, bc_user, bc_pwd)
    except:
        click.echo(colored('Error, cannot validate.', 'red'))
        click.echo('bc-host, bc-port, bc-user or bc-pwd not set in config file located at ./conf/zkRelay-cli.toml.')
        return

    if multiple_batches is not None:
        preprocessing.validateBatchesFromBlockNo(ctx,
                                                    first_block_in_batch,
                                                    multiple_batches, 
                                                    batch_size)
    else:
        preprocessing.validateBatchFromBlockNo(ctx,
                                                first_block_in_batch, 
                                                batch_size)

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
    batch_size = int(ctx.obj['zokrates_file_generator']['batch_size'])
    ctx = processBCClientConf(ctx, bc_host, bc_port, bc_user, bc_pwd)
    first_block_in_batch = block_no - (block_no % batch_size) + 1
    block_hashes = [preprocessing.littleEndian(header) for header in preprocessing.getBlockHeadersInRange(ctx, first_block_in_batch, first_block_in_batch + batch_size)]
    target_header = block_hashes[block_no % batch_size]
    tree = preprocessing.compute_full_merkle_tree(block_hashes)
    zokrates_input = preprocessing.get_proof_input(tree, target_header)
    try:
        click.echo(colored('Exec "zokrates compute-witness --light"', 'cyan'))
        subprocess.run('zokrates compute-witness --light -a ' + zokrates_input,
                        check=True, shell=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates generate-proof"', 'cyan'))
        subprocess.run('zokrates generate-proof',
                        check=True, shell=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
    except subprocess.CalledProcessError:
        click.echo('Error while computing merkle treeinclusion proof')
        click.echo(sys.exc_info()[0])
    #click.echo('%s' % result)

@zkRelay_cli.command(short_help='Generates proof validator')
@click.pass_context
def setup(ctx):
    """
    Executes 3 cmds:

    1. compile validation program

    2. generate verification keys

    3. generate smart contract that validates proofs
    """
    try:
        click.echo(colored('Exec "zokrates compile --light -i validate.zok"', 'cyan'))
        subprocess.run('zokrates compile --light -i validate.zok',
                        check=True, shell=True)
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates setup --light"', 'cyan'))
        subprocess.run('zokrates setup --light',
                        check=True, shell=True)
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates export-verifier"', 'cyan'))
        subprocess.run('zokrates export-verifier',
                        check=True, shell=True)
        click.echo(colored('Done!', 'green'))
    except subprocess.CalledProcessError:
        click.echo('Error while generating proof validator')
        click.echo(sys.exc_info()[0])

@zkRelay_cli.command(short_help='Generates merkle proof validator')
@click.pass_context
def setup_merkle_proof(ctx):
    try:
        click.echo(colored('Exec "zokrates compile --light -i verify_merkle_proof.zok"', 'cyan'))
        subprocess.run('zokrates compile --light -i verify_merkle_proof.zok',
                        check=True, shell=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates setup --light"', 'cyan'))
        subprocess.run('zokrates setup --light',
                        check=True, shell=True, cwd="mk_tree_validation/")
        click.echo(colored('Done!', 'green'))
        click.echo(colored('Exec "zokrates export-verifier"', 'cyan'))
        subprocess.run('zokrates export-verifier',
                        check=True, shell=True, cwd="mk_tree_validation/")
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
