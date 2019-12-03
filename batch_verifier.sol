pragma solidity ^0.5.0;

import "./verifier.sol" as zkVerifier;

contract BatchVerifier {

    uint256 constant batchSize = 504;
    uint256 constant epochSize = 2016;
    uint256 constant batchesInEpoch = epochSize / batchSize;

    uint256[] cumDifficultyAtBatch;
    uint256[] hashChain;
    mapping(uint256 => uint256[5]) blockHeader;

    zkVerifier.Verifier private verifier;

    struct Challenge {
        uint256 startingAtBatchHeight;
        uint256[] _cumDifficultyAtBatch;
        uint256[] _hashChain;
    }

    Challenge[] challenges;

    constructor() public {
        // add Bitcoin genesis block (little endian)
        hashChain.push(0x6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000);
        blockHeader[0x6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000] = [
        1329227995784915872903807060280344576,
        0,
        18457794364764902817207364670,
        137526082704405043163852743835310340266,
        99849781011907566316926179502243720060
        ];
        cumDifficultyAtBatch.push(0);
        verifier = new zkVerifier.Verifier();
    }

    /**
     * Assignmet of Input array variables:
     * 0 - 4:   First block of the given epoch
     * 5 - 6:   Hash of the block stored in the previous batch
     * 7 - 11:  Last block of the given batch
     * 12:      Resuålt (boolean value indicating if the batch is valid)
     * 13:      Target validity (boolean value indicating if the encoded target equals the computed target)
     * 14 - 15: Block hash of the last block in the given batch
     * 16:      Target value
     **/
    function submitBatch(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[17] memory input
    ) public returns (bool r) {
        if(!verifyBatchCorrectness(a, b, c, input, hashChain, hashChain.length, 0))
            return false;

        uint256 blockHash = from128To256(input[14], input[15]);
        hashChain.push(blockHash);
        blockHeader[blockHash] = [input[7], input[8], input[9], input[10], input[11]];

        cumDifficultyAtBatch.push(
            cumDifficultyAtBatch[cumDifficultyAtBatch.length-1] +
            difficultyFromTarget(input[16])
        );

        emit AddedNewBatchOfHeight((hashChain.length - 1) * batchSize);

        return true;
    }

    function verifyBatchCorrectness(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[17] memory input,
        uint256[] memory sourceChain,
        uint256 batchHeight,
        uint256 offset
    ) private returns (bool) {
        // Verify the correctness of the zkSNARK computation
        if(!verifier.verifyTx(a,b, c, input))
            return false;

        // Verify the correctness of the submitted headers
        if(input[12] != 1)
            return false;

        // Verify reference to previous block
        uint prev_block_hash = from128To256(input[5], input[6]);
        if(prev_block_hash != sourceChain[batchHeight - offset - 1])
            return false;

        // Every fourth batch submission, a new epoch begin
        // Verify if the target has been calculated correctly
        if(((batchHeight % batchesInEpoch) == 0) && (input[13] != 1))
            return false;

        // Verify that the correct first block of an epoch was given
        // Ensure accessing the correct chain , the fork or the main chain
        uint index = sourceChain.length + 1; // just to be sure it is oout of bounds in case anything goes wrong
        if(sourceChain.length < (batchHeight % batchesInEpoch) || sourceChain.length == hashChain.length) {
            sourceChain = hashChain;
            index = batchHeight - (batchHeight % batchesInEpoch);
        }
        else {
            batchHeight -= sourceChain.length;
            index = batchesInEpoch * (((batchHeight - sourceChain.length) % batchesInEpoch) - (batchesInEpoch - (offset % batchesInEpoch)));
        }
        // Adjust index to previous block if batch number % batchesInEpoch = 0
        if(batchHeight % batchesInEpoch == 0)
            index = index - batchesInEpoch;
        for(uint i = 0; i <= batchesInEpoch; i++) {
            if(input[i] != blockHeader[sourceChain[index]][i])
                return false;
        }

        return true;
    }

    function createMainChainChallenge(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[17] memory input,
        uint batchHeight
    ) public returns (int256 challengeId) {
        // Verify batchHeight is correct
        uint prev_block_hash = from128To256(input[5], input[6]);
        if(hashChain[batchHeight - 1] != hashChain[prev_block_hash])
            return -1;

        if(!verifyBatchCorrectness(a, b, c, input, hashChain, batchHeight, 0))
            return -1;

        uint256 difficulty = difficultyFromTarget(input[16]);
        uint256 blockHash = from128To256(input[14], input[15]);

        Challenge memory challenge = Challenge({
            startingAtBatchHeight: batchHeight,
            _cumDifficultyAtBatch: new uint256[](cumDifficultyAtBatch[batchHeight] + difficulty),
            _hashChain: new uint256[](blockHash)
            });

        challenges.push(challenge);
        challengeId = int(challenges.length - 1);
        blockHeader[blockHash] = [input[7], input[8], input[9], input[10], input[11]];

        emit AddedNewChallenge(challengeId);
    }

    function addBatchToChallenge(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[17] memory input,
        uint256 challengeId
    ) public returns (bool) {
        uint256 batchHeight = challenges[challengeId].startingAtBatchHeight + challenges[challengeId]._hashChain.length;

        if(!verifyBatchCorrectness(a, b, c, input, challenges[challengeId]._hashChain,batchHeight, challenges[challengeId].startingAtBatchHeight))
            return false;

        uint256 blockHash = from128To256(input[14], input[15]);
        challenges[challengeId]._hashChain.push(blockHash);
        blockHeader[blockHash] = [input[7], input[8], input[9], input[10], input[11]];
        challenges[challengeId]._cumDifficultyAtBatch.push(
            challenges[challengeId]._cumDifficultyAtBatch[challenges[challengeId]._cumDifficultyAtBatch.length-1] +
            difficultyFromTarget(input[16])
        );

        blockHeader[blockHash] = [input[7], input[8], input[9], input[10], input[11]];

        emit AddedNewBatchToChallenge(challengeId, challenges[challengeId]._hashChain.length);

        return true;
    }

    function settleChallenge(uint256 challengeId) public returns (bool) {
        if(challenges[challengeId]._cumDifficultyAtBatch[challenges[challengeId]._cumDifficultyAtBatch.length - 1] <=
            cumDifficultyAtBatch[cumDifficultyAtBatch.length - 1])
            return false;

        for(uint256 i = challenges[challengeId].startingAtBatchHeight; i < challenges[challengeId]._hashChain.length; i++) {
            delete blockHeader[hashChain[i]];
            hashChain[i] = challenges[challengeId]._hashChain[i - challenges[challengeId].startingAtBatchHeight];
            cumDifficultyAtBatch[i] = challenges[challengeId]._cumDifficultyAtBatch[i - challenges[challengeId].startingAtBatchHeight];
        }

        delete challenges[challengeId];

        emit SettledChallenge(challengeId);

        return true;
    }

    function difficultyFromTarget(uint256 target) private pure returns (uint256) {
        // 0x00000000FFFF00000000000000000000 is the smallest possible difficulty (cut to 128 bit from 256)
        return 0x00000000FFFF00000000000000000000 / target;
    }

    function from128To256(uint a, uint b) private pure returns (uint256) {
        return (a << 128) + b;
    }

    function getBlockHashForBlockNumber(uint number) public view returns (uint256) {
        return hashChain[number/batchSize];
    }

    function getBlockHeaderForHash(uint hash) public view returns (uint256[5] memory) {
        return blockHeader[hash];
    }

    function getBlockHeaderForBlockNumber(uint number) public view returns (uint256[5] memory) {
        getBlockHeaderForHash(getBlockHashForBlockNumber(number));
    }

    function getBatchChainLength() public view returns (uint256) {
        return hashChain.length;
    }

    function getDifficultyAtBatch(uint256 number) public view returns (uint256) {
        return cumDifficultyAtBatch[number];
    }

    event AddedNewBatchOfHeight(uint256);
    event AddedNewChallenge(int256);
    event AddedNewBatchToChallenge(uint256, uint256);
    event SettledChallenge(uint256);
}
