import re
import sys

if __name__ == "__main__":
    """
        takes batch_size and renames smart contracts according to it

        ex.:
        python3 rename_smart_contracts_and_imports.py 2
    """
    if len(sys.argv) < 2:
        exit(1)
    
    batch_size = str(sys.argv[1])

    # changing mk_tree_validation/verifier.sol
    with open('contracts/mk_tree_validation/verifier_{}.sol'.format(batch_size), 'r') as r_verifier_file:
        old_contract_content = r_verifier_file.read()

        # change BN256G2
        counter_BN256G2 = len(re.findall('BN256G2', old_contract_content))
        (new_contract_content, counter) = re.subn('BN256G2', 'BN256G2_{}'.format(batch_size), old_contract_content, count=counter_BN256G2)

        # change Verifier
        counter_Verifier = len(re.findall('Verifier', old_contract_content))
        (new_contract_content, counter) = re.subn('Verifier', 'Verifier{}'.format(batch_size), new_contract_content, count=counter_Verifier)

        # change Pairing
        counter_Pairing = len(re.findall('Pairing', old_contract_content))
        (new_contract_content, counter) = re.subn('Pairing', 'Pairing{}'.format(batch_size), new_contract_content, count=counter_Pairing)

        with open('contracts/mk_tree_validation/verifier_{}.sol'.format(batch_size), 'w') as w_verifier_file:
            w_verifier_file.write(new_contract_content)

    # changing verifier.sol
    with open('contracts/verifier_{}.sol'.format(batch_size), 'r') as r_verifier_file:
        old_contract_content = r_verifier_file.read()

        # change BN256G2
        counter_BN256G2 = len(re.findall('BN256G2', old_contract_content))
        (new_contract_content, counter) = re.subn('BN256G2', 'BN256G2_{}'.format(batch_size), old_contract_content, count=counter_BN256G2)

        # change Verifier
        counter_Verifier = len(re.findall('Verifier', old_contract_content))
        (new_contract_content, counter) = re.subn('Verifier', 'Verifier{}'.format(batch_size), new_contract_content, count=counter_Verifier)

        # change Pairing
        counter_Pairing = len(re.findall('Pairing', old_contract_content))
        (new_contract_content, counter) = re.subn('Pairing', 'Pairing{}'.format(batch_size), new_contract_content, count=counter_Pairing)

        with open('contracts/verifier_{}.sol'.format(batch_size), 'w') as w_verifier_file:
            w_verifier_file.write(new_contract_content)

    # changing batch_verifier.sol
    with open('contracts/batch_verifier_{}.sol'.format(batch_size), 'r') as r_batch_verifier_file:
        old_contract_content = r_batch_verifier_file.read()

        # change contract name, because truffle names the compiled contract after the contract name, not the file
        new_contract_content = re.sub('BatchVerifier', 'BatchVerifier{}'.format(batch_size), old_contract_content)

        # change Verifier
        counter_Verifier = len(re.findall('\.Verifier', old_contract_content))
        (new_contract_content, counter) = re.subn('\.Verifier', '.Verifier{}'.format(batch_size), new_contract_content, count=counter_Verifier)

        # change verifier import from root directory
        new_contract_content = re.sub('verifier.sol', 'verifier_{}.sol'.format(batch_size), new_contract_content)

        # change verifier import from mk_tree_validation directory
        new_contract_content = re.sub('verifier.sol', 'verifier_{}.sol'.format(batch_size), new_contract_content)

        with open('contracts/batch_verifier_{}.sol'.format(batch_size), 'w') as w_batch_verifier_file:
            w_batch_verifier_file.write(new_contract_content)