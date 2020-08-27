#!/usr/bin/env python
import sys
import click
import generate_zokrates_files as zokrates_file_generator
import preprocessing
import toml

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug',
                required=False,
                default=False,
                type=click.BOOL)
@click.pass_context
def zkRelay_cli(ctx, debug):
    """
    For more information about a command
    use 'cli COMMAND [-h, --help]'
    """
    ctx.obj = toml.load('./conf/zkRelay-cli.toml')
    pass

@zkRelay_cli.command('generate-zokrates-files')
@click.argument('batch_size',
                required=True,
                type=click.INT)
@click.pass_context
def generate_zokrates_files(ctx, batch_size):
    click.echo('Generating...')
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_validation_code(batch_size), "validate.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_root_code(batch_size), "compute_merkle_root.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_merkle_proof_validation_code(batch_size), "verify_merkle_proof.zok".format(i=batch_size))
    click.echo('Done.')
    click.echo('Updating conf file...')
    ctx.obj['zokrates_file_generator']['batch_size'] = batch_size
    toml.dump(ctx.obj, './conf/zkRelay-cli.toml')
    click.echo('Done.')

# TODO options fuer password, user, host, port fuer bitcoin client erstellen.
@zkRelay_cli.command()
@click.option('-m', '--multiple_batches',
                required=False,
                type=click.INT)
@click.argument('first_block_in_batch',
                type=click.INT)
@click.pass_context
def validate_blocks(ctx, first_block_in_batch, multiple_batches):
    batch_size = ctx.obj['batch_size']
    # TODO ctx an die functions uebergeben, sodass die sich wichtige sachen rausziehen koennen
    if multiple_batches is not None:
        preprocessing.validateBatchesFromBlockNo(first_block_in_batch,
                                                    multiple_batches, 
                                                    batch_size)
    else:
        preprocessing.validateBatchFromBlockNo(first_block_in_batch, 
                                                batch_size)

# TODO options fuer password, user, host, port fuer bitcoin client erstellen.
@zkRelay_cli.command()
@click.argument('first_block_in_batch',
                type=click.INT)
@click.pass_context
def create_input_merkle_root(ctx, first_block_in_batch):
    batch_size = ctx.obj['batch_size']
    # TODO ctx an die functions uebergeben, sodass die sich wichtige sachen rausziehen koennen
    result = preprocessing.generateZokratesInputForMerkleProof(first_block_in_batch, batch_size)
    click.echo('%s' % result)

# TODO noch einen command erstellen fuer "Compilation and Setup"
# TODO wo die 3 cmds von zokrates hintereinander weggeschaltet sind.

@zkRelay_cli.command()
@click.option('-c', '--counter', 
                default=1, 
                show_default='See zkRelay-cli.toml', 
                help='counter for function',
                required=True,
                type=click.FLOAT)
@click.argument('name', default='test')
@click.pass_context
def initdb(ctx, counter, name):
    click.echo('Initialized the database %f' % counter)

