#!/bin/bash
contract_file_path="contracts/"
cwd_smart_contracts="./../../"
cwd_truffle="tests/smartContract_tests/"

# check if smart contract has changed
python3 test/prepare_for_exec_test.py
if [[ ${cwd_smart_contracts}batch_verifier.sol -ef ./../test_data/test_smartContract/batch_verifier_reference.sol || $1 == '-c' ]]; then
    # update reference batch_verifier
    cp ${cwd_smart_contracts}batch_verifier.sol ./../test_data/test_smartContract/batch_verifier_reference.sol

    echo "Generating and compiling smart contracts and validating batches:"
    batch_sizes=(2 4)
    batch_count=(1 0)
    # ${!batch_sizes[@]} returns all indizes of array batch_sizes
    for i in ${!batch_sizes[@]}; do
        echo "For batch_size = ${batch_sizes[$i]}, batch_count = ${batch_count[$i]}"

        # go into root directory of zkRelay repository to setup dynamic test environment
        cd ${cwd_smart_contracts}

        # get amount of batches that need to be validated for the specific batch_size
        echo "Generate Smart Contract, compile zokrates program and validate batches..."
        j=0
        while [ $j -lt ${batch_count[$i]} ]; do
            batch_counter=$(expr $j + 1)

            # correct_proof_<batch_size>_<batch_count>.json
            # execute following commands:
            # zkRelay generate-files ${batch_sizes[$i]}
            # zkRelay setup
            # zkRelay validate ${batch_counter}
            python3 ${cwd_truffle}/test/compile_SM_validate_batch.py ${batch_sizes[$i]} ${batch_counter} "correct_${batch_sizes[$i]}_${batch_counter}.json"

            # Copy proofs to smartContract folder
            cp output/proof${batch_counter}.json ${cwd_truffle}test/test_data/correct_proof_${batch_sizes[$i]}_${batch_counter}.json

            # iterator
            j=$(expr $j + 1)
        done
        echo "Done."

        cp batch_verifier.sol ${cwd_truffle}${contract_file_path}batch_verifier_${batch_sizes[$i]}.sol
        cp verifier.sol ${cwd_truffle}${contract_file_path}verifier_${batch_sizes[$i]}.sol

        ## sol file in mk_tree_validation
        echo "Exec zkRelay setup-merkle-proof"
        zkRelay setup-merkle-proof #> /dev/null 2>&1
        cp mk_tree_validation/verifier.sol ${cwd_truffle}${contract_file_path}mk_tree_validation/verifier_${batch_sizes[$i]}.sol
        echo "Done."

        # Go back to truffle directory
        cd ${cwd_truffle}

        ## change imports of batch_verifier
        python3 test/rename_smart_contracts_and_imports.py ${batch_sizes[$i]}
    done
    echo "done."

    ###############################################################################
    echo "Generating files for chain challenge and merkle proof test"
    # Generating smart contracts and validating batches for chain challenge test

    ## go into root directory of zkRelay repository to setup dynamic test environment
    cd ${cwd_smart_contracts}

    ## correct_proof_<batch_size>_<batch_count>.json
    ## execute following commands:
    ## zkRelay generate-files ${batch_sizes[$i]}
    ## zkRelay setup
    ## zkRelay validate ${batch_counter}
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119640 "correct_4_119640.json"
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119641 "correct_4_119641.json"
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119642 "correct_4_119642.json"
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119643 "correct_4_119643.json"
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119644 "correct_4_119644.json"
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119645 "correct_4_119645.json"

    ## Copy proofs to smartContract folder
    cp output/proof119640.json ${cwd_truffle}test/test_data/correct_proof_4_119640.json
    cp output/proof119641.json ${cwd_truffle}test/test_data/correct_proof_4_119641.json
    cp output/proof119642.json ${cwd_truffle}test/test_data/correct_proof_4_119642.json
    cp output/proof119643.json ${cwd_truffle}test/test_data/correct_proof_4_119643.json
    cp output/proof119644.json ${cwd_truffle}test/test_data/correct_proof_4_119644.json
    cp output/proof119645.json ${cwd_truffle}test/test_data/correct_proof_4_119645.json

    ## execute for fork
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119640 "correct_4_119640_bitcoin_cash.json"
    cp output/proof119640.json ${cwd_truffle}test/test_data/correct_proof_4_119640_bitcoin_cash.json
    python3 ${cwd_truffle}/test/compile_SM_validate_batch.py 4 119641 "correct_4_119641_bitcoin_cash.json"
    cp output/proof119641.json ${cwd_truffle}test/test_data/correct_proof_4_119641_bitcoin_cash.json

    ## execute merkle proof setup and compiling
    ### setup merkle-proof
    zkRelay setup-merkle-proof #> /dev/null 2>&1
    ### compile and copy merkle-proofs
    python3 ${cwd_truffle}/test/compile_sm_merkle_proof.py 478559 4 "correct_4_119640_merkle_proof_block_3.json"
    cp mk_tree_validation/proof.json ${cwd_truffle}test/test_data/correct_proof_4_119640_merkle_proof_block_3.json
    python3 ${cwd_truffle}/test/compile_sm_merkle_proof.py 478575 4 "correct_4_119644_merkle_proof_block_3.json"
    cp mk_tree_validation/proof.json ${cwd_truffle}test/test_data/correct_proof_4_119644_merkle_proof_block_3.json

    cp batch_verifier.sol ${cwd_truffle}${contract_file_path}batch_verifier_4_chainChallenge.sol
    cp verifier.sol ${cwd_truffle}${contract_file_path}verifier_4_chainChallenge.sol

    ## sol file in mk_tree_validation
    cp mk_tree_validation/verifier.sol ${cwd_truffle}${contract_file_path}mk_tree_validation/verifier_4_chainChallenge.sol

    # Go back to truffle directory
    cd ${cwd_truffle}

    ## change imports of batch_verifier
    python3 test/rename_smart_contracts_and_imports.py 4_chainChallenge

    ## change genesis block of batch_verifier
    python3 test/change_genesis_block.py 4_chainChallenge 0x000000000000000000000000000000006934fca9a5dd15210ad36fd1898d6c0a 0x00000000000000000000000000000000c300dba0aa0148000000000000000000 0x00000000000000000000000000000000020000201082264c64bfe00b14d00731 0x0000000000000000000000000000000069508d52efeadb5b35a4e70000000000 0x0000000000000000000000000000000000000000f3ba19fccfd6fa26d1a65f0a 0x000000000000000000000000000000002885441a8f50664a4b115aefe77190f1 0x0000000000000000000000000000000014aee3289ac8795935470118c4a6d809

    ## generate malicious batches
    python3 test/create_malicious_batch_proofs.py correct_proof_4_119640.json conf_malicious_proof_4_119640_wrong_block_header.json malicious_proof_4_119640_wrong_block_header.json
    python3 test/create_malicious_batch_proofs.py correct_proof_4_119640.json conf_malicious_proof_4_119640_wrong_last_block.json malicious_proof_4_119640_wrong_last_block.json
    python3 test/create_malicious_batch_proofs.py correct_proof_4_119640.json conf_malicious_proof_4_119640_wrong_difficulty.json malicious_proof_4_119640_wrong_difficulty.json
    python3 test/create_malicious_batch_proofs.py correct_proof_4_119640.json conf_malicious_proof_4_119640_wrong_merkle_root.json malicious_proof_4_119640_wrong_merkle_root.json
    ###############################################################################
    echo "Done."
fi

# Exec actual tests
echo "Exec: truffle test"

# truffle test
./node_modules/truffle/build/cli.bundled.js test

echo "Done."
