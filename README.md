# zkRelay

zkRelay facilitates a chain-relay from Bitcoin to Ethereum through zkSNARKS.

The detailed concept of zkRelay can be found in the respective research paper published at IEEE Security & Privacy on the Blockchain 2020: [Preprint at Cryptology ePrint Archive](https://eprint.iacr.org/2020/433.pdf) / [IEEE Conference Proceedings](https://doi.org/10.1109/EuroSPW51379.2020.00058)

The implementation is based on [ZoKrates](https://github.com/Zokrates/ZoKrates) and performs off-chain Bitcoin header chain validations, while only the resulting proof is submitted to the target ledger.

The workflow of zkRelay is seperated into three steps, ZoKrates code generation, a one-time compilation and setup step and many-time validation.

As a prerequisite, [ZoKrates](https://github.com/Zokrates/ZoKrates) needs to be installed in version 0.5.1 for both steps.

## Setup zkRelay-CLI

Our cli requires you to use python version 3.

Before you install the required dependencies, we recommend to set up a venv:

``` bash
$ python3 -m venv venv
$ . venv/bin/activate
```

To install the required python dependencies and setup the CLI, run:
``` bash
$ pip3 install -r python-requirements
```

Now, you can use the cli by executing (in the venv):

``` bash
$ zkRelay
```

In `$PROJECT_DIR/conf/zkRelay-cli.toml` you can find the configuration file for the cli.

## Generate ZoKrates code

As the ZoKrates code is static for each distinct batch size, we provide a script to generate the corresponding ZoKrates code for a given batch size `n`:

``` bash
$ zkRelay generate-files n
```

## Compilation and Setup

In this step, the off-chain program is compiled, the setup for generatung proving and verification keys are executed and the smart contract verifier is generated. zkRelay integrates these three tasks in a single execution step, the setup:
``` bash
$ zkRelay setup
```
  
The resulting zkRelay contract `batch_verifier.sol` has to be deployed using a tool of your choice. It references the generated verification contract `verifier.sol` which has to be available during deployment.

## Off-chain validation


- As a prerequisite, the zkRelay-cli needs a connection to a Bitcoin client. You have two options:
  - Update the default values in the configuration file located under `$PROJECT_DIR/conf/zkRelay-cli.toml -> bitcoin_client` .
     - Possible config parameters:
        | Parameter | Description |
        --- | ---
        host | Host of BC client
        port | Port of BC client
        user | Username for access to the BC client
        pwd | Password for access to the BC client

  - Pass your overriding parameters directly to the CLI when executing the following command (see `zkRelay validate -h` for parameters)

- To validate a batch, run the following cmd, where `n` corresponds to the block number of the first block in the batch:

``` bash
$ zkRelay validate n
```

- The script retrieves the blocks from the Bitcoin client, formats them and uses ZoKrates to perform the off-chain validation. Thereafter it creates a proof for the given batch.

- The resulting witness and proof are stored in the `outputs` folder

- To retrieve a proof format that can be easily submitted, use ZoKrates' print command (the target proof has to be moved to the same directory and name `proof.json`):
``` bash
$ zokrates print-proof --format [remix, json]
```


## Create inclusion proofs for intermediary blocks

zkRelay provides a mechanism for adding intermediary blocks of previously submitted batches to the relay contract. For this purpose, a Merkle tree is generated during the off-chain block validation. The resulting Merkle root is stored within the contract. To submit an intermediary block to the contract, the Merkle root is generated within a ZoKrates program. The correctness of the off-chain execution is again validated by the relay contract. Only if the execution was correct and the computed Merkle root is equivalent with the Merkle root stored for a given batch, the submitted block header is stored. Thereafter, it can be used for securely to derive SPVs and so forth.

As the inclusion proof is conducted within a ZoKrates program, a setup is required before off-chain execusions are possible. The process is similar to the setup of the off-chain block validation program described previously.

### Setup

``` bash
$ zkRelay setup-merkle-proof
```

- The respective files are stored in the `mk_tree_validation` folder.

### Generation of inclusion proofs

- To generate an inclusion proof for a block with block number n, execute the following cmd:

``` bash
$ zkRelay create-merkle-proof n
```

- The proof is stoed in `./mk_tree_validation/proof.json`
- To retrieve a proof format that can be easily submitted, use ZoKrates' print command from within the `mk_tree_validation` folder:

``` bash
$ zokrates print-proof --format [remix, json]
```

## Development Environment

### Setup

Before you install the required dependencies, we recommend to set up a venv:

``` bash
$ python3 -m venv venv
$ . venv/bin/activate
```

To install the required python dependencies for development, run:
``` bash
$ pip3 install -r dev-python-requirements
```

This mainly installs additional packages that are needed for the test environment.
Furthermore it sets the editable flag when installing. That way, source files are linked
together and used for execution of the CLI. Changes in source files can therefor directly get tested
and used without having to install zkRelay again.

We use the truffle test suite for our smart contract test cases. Before you can execute the tests, you need to go to the smartContract_test folder and install all required packages:

```bash
$ cd {Project_root}/tests/smartContract_tests
$ npm install
```

### Tests

#### Python Scripts

NOTE: Make sure that you are on the project root in your terminal!

We use the module `unittest` for our test cases. You can execute all tests with the following command:

``` bash
$ python3 -m unittest
```

If you want to test specific test files or test cases you can do so by just calling them like packages.

Lets say you want to test malicious input for the zkRelay command validate, then you would execute the following:

``` bash
$ python -m unittest tests.cmd_validate_tests.test_malicious_blocks.TestMaliciousBlocks
```

If you only want to test one test case, e.g. test_7_crossover_of_epochs, your command would like like the following:

``` bash
$ python -m unittest tests.cmd_validate_tests.test_malicious_blocks.TestMaliciousBlocks.test_7_crossover_of_epochs
```

#### Smart Contract

You can execute tests for the smart contracts inside of the smartContract_tests folder with the following commands:

``` bash
$ cd {Project_root}/tests/smartContract_tests/
$ npm run test
```