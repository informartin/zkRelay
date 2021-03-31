// when compiling, batch_verfier becomes BatchVerifier, that's why we need to require BatchVerifier instead here.
const Batch_Verifier2 = artifacts.require('BatchVerifier2');
const fs = require('fs');
const { expectEvent, expectRevert, BN } = require('@openzeppelin/test-helpers');
const { expect } = require('chai');

const test_data_path = 'test/test_data/'

contract('BatchVerifier2', (accounts) => {
    let batch_verifier_instance;

    beforeEach(async() => {
        // need to manually get a new instance of our contract for each test.
        // 'clean room environment' from truffle is failing.
        batch_verifier_instance = await Batch_Verifier2.new();
    });

    it('should accept correct batch of 2 blocks', async () => {
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_2_1.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('85878663077284866801469176824632952841341549244818799940625725638586142818304'));
    });

    it('should refuse malicious batch of 2 blocks', async () => {
        /*
         * tests a batch that is validated through a valid but wrong zksnarks program
         */
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}outdated_2.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert.unspecified(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs)
        );

        // check for latest block hash
        const receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('50607000162736768413865283251298348907857627207201349845683772230799839985664'));
    });
});