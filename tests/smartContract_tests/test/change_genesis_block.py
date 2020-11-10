import sys
import re

def from128to256(a, b):
    return (a << 128) + b

if __name__ == "__main__":
    """
        takes block information given and changes genesis block according to it

        @parameters:
        - file_name_suffix (what is written behind batch_verifier)
        - block_header_hash_a
        - block_header_hash_b
        - block_header_1
        - block_header_2
        - block_header_3
        - block_header_4
        - block_header_5

        ex.:
        python3 change_genesis_block.py 4_chainChallenge 0x00000000000000000000000000000000432d350741fbf28f2e1486eabe2c4e14 0x000000000000000000000000000000003bfe2241af6518010000000000000000
        0x0000000000000000000000000000000002000020e42980330b7294bef6527af5 0x0000000000000000000000000000000076e5cfe2c97d55f9c19beb0000000000 0x00000000000000000000000000000000000000004a88016082f466735a0f4bc9 0x00000000000000000000000000000000e5e42725fbc3d0ac28d4ab9547bf1865 0x000000000000000000000000000000004f14655b1e7f80593547011816dd5975
    """
    if len(sys.argv) < 9:
        exit(1)

    file_name_suffix = str(sys.argv[1])

    with open('contracts/batch_verifier_{}.sol'.format(file_name_suffix), 'r') as r_batch_verifier_file:
        old_contract_content = r_batch_verifier_file.read()

        # change header hash
        block_header_hash = hex(from128to256(int(sys.argv[2], base=16), int(sys.argv[3], base=16)))
        new_contract_content = re.sub('batch.headerHash = 0x\w+;', 'batch.headerHash = {};'.format(block_header_hash), old_contract_content)

        # change block header
        block_header_1 = int(sys.argv[4], base=16)
        block_header_2 = int(sys.argv[5], base=16)
        block_header_3 = int(sys.argv[6], base=16)
        block_header_4 = int(sys.argv[7], base=16)
        block_header_5 = int(sys.argv[8], base=16)
        new_contract_content = re.sub('batch.blockHeader = .+\n.+\n.+\n.+\n.+\n.+\n.+;', 'batch.blockHeader = [{},{},{},{},{}];'.format(block_header_1, block_header_2, block_header_3, block_header_4, block_header_5), new_contract_content)

        with open('contracts/batch_verifier_{}.sol'.format(file_name_suffix), 'w') as w_batch_verifier_file:
            w_batch_verifier_file.write(new_contract_content)
