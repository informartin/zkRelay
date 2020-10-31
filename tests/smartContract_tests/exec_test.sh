#!/bin/bash
contract_file_path="contracts/"
cwd_smart_contracts="./../../"
cwd_truffle="tests/smartContract_tests/"

echo "Generating and compiling smart contracts and validating batches:"
batch_sizes=(2 4)
batch_count=(1 0)
# TODO do the following in a loop for copying smart contracts with differenct batch sizes
# ${!batch_sizes[@]} returns all indizes of array batch_sizes
for i in ${!batch_sizes[@]}; do
    echo "For batch_size = ${batch_sizes[$i]}, batch_count = ${batch_count[$i]}"

    # go into root directory of zkRelay repository to setup dynamic test environment
    cd ${cwd_smart_contracts}

    # get amount of batches that need to be validated for the specific batch_size
    echo "Generate Smart Contract, compile zokrates program and validate batches..."
    j=0
    while [ $j -lt ${batch_count[$i]} ]; do
        batch_counter=`expr $j + 1`

        # correct_proof_<batch_size>_<batch_count>.json
        # execute following commands:
        # zkRelay generate-files ${batch_sizes[$i]}
        # zkRelay setup
        # zkRelay validate ${batch_counter}
        python3 ${cwd_truffle}/test/compile_SM_validate_batch.py ${batch_sizes[$i]} ${batch_counter} "correct_${batch_sizes[$i]}_${batch_counter}.json"
        
        # Copy smart contracts and proofs to smartContract folder
        cp output/proof${batch_counter}.json ${cwd_truffle}test/test_data/correct_proof_${batch_sizes[$i]}_${batch_counter}.json

        # iterator
        j=`expr $j + 1`
    done
    echo "Done."

    cp batch_verifier.sol ${cwd_truffle}${contract_file_path}batch_verifier_${batch_sizes[$i]}.sol
    cp verifier.sol ${cwd_truffle}${contract_file_path}verifier_${batch_sizes[$i]}.sol

    ## sol file in mk_tree_validation
    cp mk_tree_validation/verifier.sol ${cwd_truffle}${contract_file_path}mk_tree_validation/verifier_${batch_sizes[$i]}.sol

    # Go back to truffle directory
    cd ${cwd_truffle}

    ## change imports of batch_verifier
    python3 test/rename_smart_contracts_and_imports.py ${batch_sizes[$i]}
done

echo "Done."

# Exec actual tests
echo "Exec: truffle test"

truffle test

echo "Done."