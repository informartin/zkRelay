// SPDX-License-Identifier: LGPL-3.0-or-later
pragma solidity ^0.5.0;

import "./verifier.sol" as zkVerifier;
import "./mk_tree_validation/verifier.sol" as mkVerifier;

contract BatchVerifier {

    uint256 constant BATCH_SIZE = 4;
    uint256 constant EPOCH_SIZE = 2016;
    uint256 constant BATCHES_IN_EPOCH = EPOCH_SIZE / BATCH_SIZE;

    struct Batch {
        uint256 headerHash; // Hash of last block header included in batch
        uint256[5] blockHeader;
        uint256 cumDifficulty;
        uint256 merkleRoot;
        mapping(uint256 => uint256[5]) intermediaryHeader;
    }
    
    struct Branch {
        uint256 startingAtBatchHeight;
        //Batch[] batchChain;
        uint numBatchChain;
        mapping (uint => Batch) batchChain;
    }

    // Not possible, as nested arrays in structs are not available in solidity versions > 0.7
    //Branch[] hashChains;
    uint numBranches;
    mapping (uint => Branch) branches;

    zkVerifier.Verifier private verifier;
    mkVerifier.Verifier private mkTreeVerifier;

    constructor() public {
        // add Bitcoin genesis block (little endian)
        Branch storage mainChain = branches[numBranches++];
        Batch storage batch = mainChain.batchChain[mainChain.numBatchChain++];
        batch.headerHash = 0x6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000;

        batch.blockHeader = [
            1329227995784915872903807060280344576,
            0,
            18457794364764902817207364670,
            137526082704405043163852743835310340266,
            99849781011907566316926179502243720060
        ];
        verifier = new zkVerifier.Verifier();
        mkTreeVerifier = new mkVerifier.Verifier();
    }
    
    
    /**
     * Assignmet of Input array variables:
     * 0:       First block of the given epoch
     * 1 - 2:   Hash of the block stored in the previous batch
     * 3 - 7:   Last block of the given batch
     * 8:       Result (boolean value indicating if the batch is valid)
     * 9:       Target validity (boolean value indicating if the encoded target equals the computed target)
     * 10 - 11: Block hash of the last block in the given batch
     * 12:      Target value
     * 13 - 14: Merkle root
     **/
    function submitBatch(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[15] memory input
    ) public returns (bool r) {
        require(verifyBatchCorrectness(a, b, c, input, 0, branches[0].numBatchChain, 0), 'Could not verify batch correctness');
        
        Branch storage mainChain = branches[0];
        Batch storage batch = mainChain.batchChain[mainChain.numBatchChain];
        
        createBatch(input, mainChain, batch);

        emit AddedNewBatch((branches[0].numBatchChain - 1));

        return true;
    }

    function verifyBatchCorrectness(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[15] memory input,
        uint branchId,
        uint256 batchHeight,
        uint256 offset
    ) private returns (bool) {
        // Verify the correctness of the zkSNARK computation
        require(verifier.verifyTx(a,b, c, input), 'Could not verify tx');

        // Verify the correctness of the submitted headers
        require(input[8] == 1, 'Submitted headers are not correct');

        // Verify reference to previous block
        uint prev_block_hash = from128To256(input[1], input[2]);
        require(prev_block_hash == branches[branchId].batchChain[batchHeight - offset - 1].headerHash, 'Previous block hash is not correct');

        // Every fourth batch submission, a new epoch begin
        // Verify if the target has been calculated correctly
        require(((batchHeight % BATCHES_IN_EPOCH) != 0) || (((batchHeight % BATCHES_IN_EPOCH) == 0) && (input[9] == 1)), 'Target was not calculated correctly.');

        // Verify that the correct first block of an epoch was given
        // Ensure accessing the correct chain , the fork or the main chain
        uint index = branches[branchId].numBatchChain + 1; // just to be sure it is out of bounds in case anything goes wrong
        if(branches[branchId].numBatchChain < (batchHeight % BATCHES_IN_EPOCH) || branches[branchId].numBatchChain == branches[0].numBatchChain) {
            branchId = 0;
            index = batchHeight - (batchHeight % BATCHES_IN_EPOCH);
        } else {
            batchHeight -= branches[branchId].numBatchChain;
            index = BATCHES_IN_EPOCH * (((batchHeight - branches[branchId].numBatchChain) % BATCHES_IN_EPOCH) - (BATCHES_IN_EPOCH - (offset % BATCHES_IN_EPOCH)));
        }
        // Adjust index to previous block if batch number % BATCHES_IN_EPOCH = 0
        if(batchHeight % BATCHES_IN_EPOCH == 0)
            index = index - BATCHES_IN_EPOCH;
        // To save gas costs, only the relevant fifth field element of the epoch head is passed as parameter
        require(input[0] == branches[branchId].batchChain[index].blockHeader[4], 'Epoch block ist not correct.');

        return true;
    }

    function createMainChainChallenge(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[15] memory input,
        uint batchHeight
    ) public returns (uint256 challengeId) {
        // Verify batchHeight is correct
        uint prev_block_hash = from128To256(input[1], input[2]);
        require(branches[0].batchChain[batchHeight - 1].headerHash == prev_block_hash, 'The submitted previous block hash is not the same as the block at the batchHeight on the main chain.');
        require(verifyBatchCorrectness(a, b, c, input, 0, batchHeight, 0), 'Could not verify batch for challenging fork.');

        Branch storage challengeChain = branches[numBranches];
        Batch storage genesisBatch = challengeChain.batchChain[challengeChain.numBatchChain++];
        Batch storage batch = challengeChain.batchChain[challengeChain.numBatchChain];
        challengeChain.startingAtBatchHeight = batchHeight;
        
        // add 'genesis block' to new challenging chain
        genesisBatch.cumDifficulty = branches[0].batchChain[batchHeight - 1].cumDifficulty;

        createBatch(input, challengeChain, batch);

        emit AddedNewChallenge(numBranches);
        
        return numBranches++;
    }

    function addBatchToChallenge(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[15] memory input,
        uint256 challengeId
    ) public returns (bool) {
        uint256 batchHeight = branches[challengeId].startingAtBatchHeight + branches[challengeId].numBatchChain;

        require(verifyBatchCorrectness(a, b, c, input, challengeId ,batchHeight, branches[challengeId].startingAtBatchHeight), 'Could not verify batch for challenging fork.');

        Branch storage challengeChain = branches[challengeId];
        Batch storage batch = challengeChain.batchChain[challengeChain.numBatchChain];

        createBatch(input, challengeChain, batch);

        // -1 because of 'genesis block' on challenging chain
        emit AddedNewBatchToChallenge(challengeId, branches[challengeId].numBatchChain - 1);

        return true;
    }

    function settleChallenge(uint256 challengeId) public returns (bool) {
        uint256 cumDifficulty_ChallengeChain = branches[challengeId].batchChain[branches[challengeId].numBatchChain - 1].cumDifficulty;
        uint256 cumDifficulty_MainChain = branches[0].batchChain[branches[0].numBatchChain - 1].cumDifficulty;
        require(cumDifficulty_ChallengeChain > cumDifficulty_MainChain, 'Not enough proof of work on challenging chain.');

        Branch storage mainBranch = branches[0];
        Branch storage challengingBranch = branches[challengeId];
        for(uint256 i = branches[challengeId].startingAtBatchHeight; i <= branches[challengeId].numBatchChain; i++) {
            // overwriting chain with blocks of challenging chain
            // +1 because of 'genesis block' on challenging chain
            mainBranch.batchChain[i] = challengingBranch.batchChain[i - challengingBranch.startingAtBatchHeight + 1];

            // deleting blocks from challenging chain as they are no longer needed
            delete challengingBranch.batchChain[i - challengingBranch.startingAtBatchHeight];
        }

        // update numBatchChain of main chain to new length
        // -1 because of 'genesis block' on challenging chain
        mainBranch.numBatchChain = challengingBranch.startingAtBatchHeight + challengingBranch.numBatchChain - 1;

        delete branches[challengeId];

        emit SettledChallenge(challengeId);

        return true;
    }

    function createBatch(uint[15] memory input, Branch storage chain, Batch storage batch) internal {
        uint256 blockHash = from128To256(input[10], input[11]);
        uint256 difficulty = difficultyFromTarget(input[12]);
        uint256 merkleRoot = from128To256(input[13], input[14]);
        
        batch.headerHash = blockHash;
        batch.cumDifficulty = chain.batchChain[chain.numBatchChain - 1].cumDifficulty + difficulty;
        batch.merkleRoot = merkleRoot;
        batch.blockHeader = [input[3], input[4], input[5], input[6], input[7]];
        chain.numBatchChain++;
    }
    
    /*
    * Assignmet of Input array variables:
    * 0 - 4: Block header
    * 5 - 6: Block header hash
    * 7 - 8: Computed Merkle Root
    */
    function submitIntermediaryBlock(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[9] memory input,
        uint batchNo) public {
            require(mkTreeVerifier.verifyTx(a, b, c, input), 'Could not verify tx');
            
            uint256 merkleRoot = from128To256(input[7], input[8]);
            uint256 headerHash = from128To256(input[5], input[6]);
            Batch storage batch = branches[0].batchChain[batchNo];
            require(batch.merkleRoot == merkleRoot, 'Merkle root of request is not the same as merkle root of batch');
            batch.intermediaryHeader[headerHash] = [input[0], input[1], input[2], input[3], input[4]];

            emit AddedNewIntermediaryBlock(batchNo, headerHash);
        }

    function difficultyFromTarget(uint256 target) private pure returns (uint256) {
        // 0x00000000FFFF00000000000000000000 is the smallest possible difficulty (cut to 128 bit from 256)
        return 0x00000000FFFF00000000000000000000 / target;
    }

    function from128To256(uint a, uint b) private pure returns (uint256) {
        return (a << 128) + b;
    }
    
    function getLatestBlockHash(uint branchId) public view returns (uint256) {
        return branches[branchId].batchChain[branches[branchId].numBatchChain - 1].headerHash;
    }
    
    // hash must be little endian!
    function getBlockBlockHeader(uint256 number, uint256 hash) public view returns (uint256[5] memory header) {
        Batch storage batch = branches[0].batchChain[number / BATCH_SIZE + 1];
        if (number % BATCH_SIZE == 0)
            return batch.blockHeader;
        else
            return batch.intermediaryHeader[hash];
    }
    
    function getMerkleRoot(uint batchNo) public view returns (uint256) {
        return branches[0].batchChain[batchNo].merkleRoot;
    }
    
    function getSnarkVerifier() public view returns (address) {
        return address(verifier);
    }

    event TestEvent(bool);
    event AddedNewBatch(uint256 batchHeight);
    event AddedNewChallenge(uint256 challengeID);
    event AddedNewBatchToChallenge(uint256 challengeID, uint256 batchHeight);
    event AddedNewIntermediaryBlock(uint256 batchNo, uint256 headerHash);
    event SettledChallenge(uint256 challengeID);
}
