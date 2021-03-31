const BatchVerifier4_chainChallenge = artifacts.require('BatchVerifier4_chainChallenge');
const fs = require('fs');
const { expectEvent, expectRevert, BN } = require('@openzeppelin/test-helpers');
const { expect } = require('chai');

const test_data_path = 'test/test_data/'

contract('Merkle Proof', (accounts) => {
    let batch_verifier_instance;

    beforeEach(async() => {
        // need to manually get a new instance of our contract for each test.
        // 'clean room environment' from truffle is failing.
        batch_verifier_instance = await BatchVerifier4_chainChallenge.new();
    });

    it('should accept valid merkle proof of third block in a batch of 4 (block_no = 478559)', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // check for event
        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_merkle_proof_block_3.json`, 'utf-8'));

        // submit merkle proof to smart contract
        receipt = await batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewIntermediaryBlock', { '0': new BN(1), '1': new BN('32851869952590920346242081961869266619787065709022915434753342925090647441408')});

        receipt = await batch_verifier_instance.getBlockBlockHeader(3, new BN('32851869952590920346242081961869266619787065709022915434753342925090647441408'));

        expect(receipt[0]).to.be.bignumber.equal(new BN('2658458547661179941484656166939428586'), 'block header hash[0] of the intermediary block is not the expected one.');
        expect(receipt[1]).to.be.bignumber.equal(new BN('252783363891988727892737294594285240320'), 'block header hash[1] of the intermediary block is not the expected one.');
        expect(receipt[2]).to.be.bignumber.equal(new BN('7597124451856150362625841682'), 'block header hash[2] of the intermediary block is not the expected one.');
        expect(receipt[3]).to.be.bignumber.equal(new BN('114340279030832607808183600780233688421'), 'block header hash[3] of the intermediary block is not the expected one.');
        expect(receipt[4]).to.be.bignumber.equal(new BN('32143692016862878434268072100902047159'), 'block header hash[4] of the intermediary block is not the expected one.');
    });

    it('should accept valid merkle proof inside of a bigger chain (block_no = 478575)', async () => {
        // first, add data to mainChain
        let data;
        let receipt;
        for (let i = 0; i < 6; i++) {
            // get test_data
            data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_11964${i}.json`, 'utf-8'));

            // submit batch to smart contract
            receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

            // check for event
            expectEvent(receipt, 'AddedNewBatch', { '0': new BN(i + 1) });
        }

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119644_merkle_proof_block_3.json`, 'utf-8'));

        // submit merkle proof to smart contract
        receipt = await batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 5);

        expectEvent(receipt, 'AddedNewIntermediaryBlock', { '0': new BN(5), '1': new BN('45902873511293823114585154393118010637119071233357617220353159420012188925952')});

        receipt = await batch_verifier_instance.getBlockBlockHeader(18, new BN('45902873511293823114585154393118010637119071233357617220353159420012188925952'));

        expect(receipt[0]).to.be.bignumber.equal(new BN('2658458604002811340345573574474321373'), 'block header hash[0] of the intermediary block is not the expected one.');
        expect(receipt[1]).to.be.bignumber.equal(new BN('227845122133096928877911758674902122496'), 'block header hash[1] of the intermediary block is not the expected one.');
        expect(receipt[2]).to.be.bignumber.equal(new BN('66477530704985583731752246740'), 'block header hash[2] of the intermediary block is not the expected one.');
        expect(receipt[3]).to.be.bignumber.equal(new BN('112626912128255033793213597511645447907'), 'block header hash[3] of the intermediary block is not the expected one.');
        expect(receipt[4]).to.be.bignumber.equal(new BN('119130702145458319987686862029185616026'), 'block header hash[4] of the intermediary block is not the expected one.');
    });

    it('should not accept a merkle proof from another verifier (third block in a batch of 4 of batch_no=119640) (block_no = 478559)', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // check for event
        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}outdated_4_119640_merkle_proof_block_3.json`, 'utf-8'));

        // submit merkle proof to smart contract
        await expectRevert(
            batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1),
            'Could not verify tx'
        );
    });

    it('should not accept a valid merkle proof from another batch', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // check for event
        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119644_merkle_proof_block_3.json`, 'utf-8'));

        await expectRevert.unspecified(
            batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1)
        );
    });

    // it('should not accept a merkle proof that was already submitted', async () => {
    //     // get test_data
    //     let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

    //     // submit batch to smart contract
    //     let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

    //     // check for event
    //     expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

    //     // get test_data
    //     data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_merkle_proof_block_3.json`, 'utf-8'));

    //     // submit merkle proof to smart contract
    //     receipt = await batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

    //     await expectRevert.unspecified(
    //         batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1)
    //     );
    // });

    it('should not accept a merkle proof of a batch that was not submitted until now', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_merkle_proof_block_3.json`, 'utf-8'));

        await expectRevert.unspecified(
            batch_verifier_instance.submitIntermediaryBlock(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1)
        );
    });
});