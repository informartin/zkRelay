import re
import pathlib

if __name__ == "__main__":
    with open('./../../batch_verifier.sol', 'r') as r_batch_verifier_file:
        # get batch_size of smart contract and replace batch_size in reference contract
        curr_contract = r_batch_verifier_file.read()
        batch_size_search = re.search('BATCH_SIZE = (\d+)', curr_contract)
        
        batch_size = int(batch_size_search.group(1))

        # save new content with updated batch_size
        with open('./../test_data/test_smartContract/batch_verifier_reference.sol', 'r') as r_batch_verifier_reference_file:
            reference_contract = r_batch_verifier_reference_file.read()

            reference_contract = re.sub('BATCH_SIZE = \d+', 'BATCH_SIZE = {}'.format(batch_size), reference_contract)

            with open('./../test_data/test_smartContract/batch_verifier_reference.sol', 'w+') as w_file:
                w_file.write(reference_contract)