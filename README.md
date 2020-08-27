# zkRelay

zkRelay facilitates a chain-relay from Bitcoin to Ethereum through zkSNARKS.

The implementation is based on [ZoKrates](https://github.com/Zokrates/ZoKrates) and performs off-chain Bitcoin header chain validations, while only the resulting prrof is submitted to the target ledger.
The main branch of this repository includes an implementation that performs batch validations for 63 Bitcoin blocks.

The workflow of zkRelay is seperated into three steps, ZoKrates code generation, a one-time compilation and setup step and many-time validation.

As a prerequisite, [ZoKrates](https://github.com/Zokrates/ZoKrates) needs to be installed for both steps.

## Setup zkRelay-CLI and env

Before you install the required dependencies, we recommend to set up a venv:

``` bash
$ virtualenv venv
$ . venv/bin/activate
```

To install the required python dependencies and setup the CLI, run:
``` bash
$ pip3 install --editable .
```

Now, you can use the cli by executing (in the venv):

``` bash
$ zkRelay-cli
```

In `$PROJECT_DIR/conf/zkRelay-cli.toml` you can find the configuration file for the cli.

## Generate ZoKrates code

As the ZoKrates code is static for each distinct batch size, we provide a script to generate the corresponding ZoKrates code for a given batch size `n`:

``` bash
$ zkRelay-cli generate-zokrates-files n
```

## Compilation and Setup

With the zkRelay-cli command `zkRelay-cli compile-and-generate-proof-validator` we start an execution pipeline of three ZoKrates cmds:

- First, the off-chain validation program has to be compiled:

``` bash
$ zokrates compile --light -i validate.zok
```

- Second, the proving and verfication keys are generated in the setup step:

``` bash
$ zokrates setup --light
```

- Third, a smart contract is generated that validates proofs:

``` bash
$ zokrates export-verifier
```
  
The resulting zkRelay contract `batch_verifier.sol` has to be deployed using a tool of your choice. It references the generated verification contract `verifier.sol` which has to be available during deployment.

## Off-chain validation


- As a prerequisite, the zkRelay-cli needs a connection to a Bitcoin client. You have two options:
  1. Update the default values in the configuration file located under `$PROJECT_DIR/conf/zkRelay-cli.toml`.
  2. Pass your overriding parameters directly to the CLI when executing the following command.

- To validate a batch, run the following cmd, where `n` corresponds to the block number of the first block in the batch:

``` bash
$ zkRelay-cli validate-blocks n
```

- The script retrieves the blocks from the Bitcoin client, formats them and uses ZoKrates to perform the off-chain validation. Thereafter it creates a proof for the given batch.

- The resulting witness and proof are stored in the `outputs` folder

- To retrieve a proof format that can be easily submitted, use ZoKrates' print command (the target proof has to be moved to the same directory and name `proof.json`):

  `zokrates print-proof --format [remix, json]`
