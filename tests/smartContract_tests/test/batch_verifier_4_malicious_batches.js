const BatchVerifier4_chainChallenge = artifacts.require('BatchVerifier4_chainChallenge');
const fs = require('fs');
const { expectEvent, expectRevert, BN } = require('@openzeppelin/test-helpers');
const { expect } = require('chai');

const test_data_path = 'test/test_data/'

contract('Malicious Batches', (accounts) => {
    let batch_verifier_instance;

    beforeEach(async() => {
        // need to manually get a new instance of our contract for each test.
        // 'clean room environment' from truffle is failing.
        batch_verifier_instance = await BatchVerifier4_chainChallenge.new();
    });

    it('should not accept malicious batch of 4 blocks with wrong block header', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}malicious_proof_4_119640_wrong_block_header.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs),
            'Could not verify tx'
        );
    });

    it('should not accept malicious batch of 4 blocks with wrong last block', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}malicious_proof_4_119640_wrong_last_block.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs),
            'Could not verify tx'
        );
    });

    it('should not accept malicious batch of 4 blocks with wrong merkle root', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}malicious_proof_4_119640_wrong_merkle_root.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs),
            'Could not verify tx'
        );
    });

    it('should not accept malicious batch of 4 blocks with wrong difficulty', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}malicious_proof_4_119640_wrong_difficulty.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert.unspecified(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs)
        );
    });
});