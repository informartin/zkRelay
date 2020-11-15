const BatchVerifier4_chainChallenge = artifacts.require('BatchVerifier4_chainChallenge');
const fs = require('fs');
const { expectEvent, expectRevert, BN } = require('@openzeppelin/test-helpers');
const { expect } = require('chai');

const test_data_path = 'test/test_data/'

contract('BatchVerifier4_chainChallenge', (accounts) => {
    let batch_verifier_instance;

    beforeEach(async() => {
        // need to manually get a new instance of our contract for each test.
        // 'clean room environment' from truffle is failing.
        batch_verifier_instance = await BatchVerifier4_chainChallenge.new();
    });

    it('should accept correct batch of 4 blocks on main chain with adjusted genesis block', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('23800915914239488861140398695137368811614411938412653098089824453839145664512'));
    });

    it('should accept correct batch of 4 blocks from fork', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_bitcoin_cash.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('55700842284869722127662445745006925938356530809612975865941298128392086880256'));
    });

    it('should accept a new challenging chain (fork)', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewChallenge', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(1);

        expect(receipt).to.be.bignumber.equal(new BN('23800915914239488861140398695137368811614411938412653098089824453839145664512'));
    });

    it('should not accept wrong batch for a new challenging chain (fork)', async () => {
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119641.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert.unspecified(
            batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1)
        );
    });


    it('should not accept a new challenging chain with same blocks as existing challenging chain', async () => {
        // first, create chainChallenge
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewChallenge', { '0': new BN(1) });

        // second, try to create same chainChallenge
        // get test data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119641.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert.unspecified(
            batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 2)
        );
    });

    it('should not accept batch submission that was validated through another verifier for createMainChainChallenge', async () => {
        // first, create chainChallenge
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}outdated_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        await expectRevert(
            batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1),
            'Could not verify tx.'
        );
    });

    it('should not accept batch submission that was validated through another verifier for addBatchToChallenge', async () => {
        // first, create chainChallenge
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        data = JSON.parse(fs.readFileSync(`${test_data_path}outdated_4_119641.json`, 'utf-8'));

        await expectRevert(
            batch_verifier_instance.addBatchToChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1),
            'Could not verify tx.'
        );
    });

    it('should addBatchToChallenge', async () => {
        // first, create chainChallenge
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewChallenge', { '0': new BN(1) });

        // second, addBatchToChallenge
        // get test data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119641.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.addBatchToChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewBatchToChallenge', { '0': new BN(1), '1': new BN(2) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(1);

        expect(receipt).to.be.bignumber.equal(new BN('76897399149429910857920006940948127779674830872108457539135840393891636314112'));
    });

    it('should accept a new challenging chain next to existing mainChain', async () => {
        // first, add data to mainChain
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_bitcoin_cash.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        expectEvent(receipt, 'AddedNewBatch', { '0': new BN(1) });

        // second, add data 
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        expectEvent(receipt, 'AddedNewChallenge', { '0': new BN(1) });


        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(1);

        expect(receipt).to.be.bignumber.equal(new BN('23800915914239488861140398695137368811614411938412653098089824453839145664512'));

    });

    it('should settleChallenge', async () => {
        // first, add data to mainChain
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_bitcoin_cash.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // second, create mainChainChallenge
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        // third, add more data to challenging chain
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119641.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.addBatchToChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        // fourth, exec settle settleChallenge
        receipt = await batch_verifier_instance.settleChallenge(1);

        expectEvent(receipt, 'SettledChallenge', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('76897399149429910857920006940948127779674830872108457539135840393891636314112'));
    });

    it('should settleChallenge with longer chain', async () => {
        // first, add data to mainChain
        let data;
        let receipt;
        for (let i = 0; i < 2; i++) {
            // get test_data
            data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_11964${i}_bitcoin_cash.json`, 'utf-8'));

            // submit batch to smart contract
            receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

            // check for event
            expectEvent(receipt, 'AddedNewBatch', { '0': new BN(i + 1) });
        }
        
        // second, create mainChainChallenge
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        // third, add much more data to challenging chain
        for (let i = 1; i < 6; i++) {
            // get test_data
            data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_11964${i}.json`, 'utf-8'));

            // submit batch to smart contract
            receipt = await batch_verifier_instance.addBatchToChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

            // check for event 
            expectEvent(receipt, 'AddedNewBatchToChallenge', { '0': new BN(1), '1': new BN(1 + i) });
        }

        // check for latest block hash on side chain
        receipt = await batch_verifier_instance.getLatestBlockHash(1);
        expect(receipt).to.be.bignumber.equal(new BN('673543456807305701500678383248570431861705562909382717589122311334867763200'))

        // fourth, exec settle settleChallenge
        receipt = await batch_verifier_instance.settleChallenge(1);

        expectEvent(receipt, 'SettledChallenge', { '0': new BN(1) });

        // check for latest block hash
        receipt = await batch_verifier_instance.getLatestBlockHash(0);

        expect(receipt).to.be.bignumber.equal(new BN('673543456807305701500678383248570431861705562909382717589122311334867763200'));
    });

    it('should not settleChallenge if not enough proof of work', async () => {
        // first, add data to mainChain
        // get test_data
        let data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640.json`, 'utf-8'));

        // submit batch to smart contract
        let receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // second, add data to mainChain
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119641.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.submitBatch(data.proof.a, data.proof.b, data.proof.c, data.inputs);

        // third, create mainChainChallenge
        // get test_data
        data = JSON.parse(fs.readFileSync(`${test_data_path}correct_proof_4_119640_bitcoin_cash.json`, 'utf-8'));

        // submit batch to smart contract
        receipt = await batch_verifier_instance.createMainChainChallenge(data.proof.a, data.proof.b, data.proof.c, data.inputs, 1);

        // fourth, try to exec settle settleChallenge
        await expectRevert(
            batch_verifier_instance.settleChallenge(1),
            'Not enough proof of work on challenging chain.'
        );
    });
});