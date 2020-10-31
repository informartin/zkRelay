// when compiling, batch_verfier becomes BatchVerifier, that's why we need to require BatchVerifier instead here.
const Batch_Verifier2 = artifacts.require('BatchVerifier2');
const fs = require('fs');
const { expectEvent, expectRevert, BN } = require('@openzeppelin/test-helpers');

const test_data_path = 'test/test_data/'

contract('BatchVerifier2', (accounts) => {
    it('should accept correct batch of 2 blocks', async () => {
        const batch_verifier_instance = await Batch_Verifier2.deployed();

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_2_1.json`, 'utf-8'));

        // submit batch to smart contract
        const receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        expectEvent(receipt, 'AddedNewBatchOfHeight', { '0': new BN(2) });
    });

    it('should refuse malicious batch of 2 blocks', async () => {
        /*
         * tests a batch that is validated through a wrong zksnarks program
         */
        const batch_verifier_instance = await Batch_Verifier2.deployed();

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}outdated_2.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert.unspecified(
            batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs));

        // await expectRevert(
        //     batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs),
        //     expectRevert.unspecified()
        // );
    });
});