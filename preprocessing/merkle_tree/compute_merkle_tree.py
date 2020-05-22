from pycrypto.zokrates_pycrypto.gadgets.pedersenHasher import PedersenHasher
from pycrypto.zokrates_pycrypto.babyjubjub import Point
import math

def compute_merkle_tree(leafs):
    hasher = PedersenHasher(b"test")
    tree = []
    for i in range(0, len(leafs), 2):
        left = leafs[i]
        right = leafs[i+1] if i != len(leafs) - 1 else left
        preimage = bytes.fromhex(left + right)
        digest = hasher.hash_bytes(preimage)
        compressedDigest = Point.compress(digest).hex()
        tree.append(compressedDigest)

    if len(leafs) > 2:
        tree.extend(compute_merkle_tree(tree))

    return tree

def compute_full_merkle_tree_helper(leafs):
    hasher = PedersenHasher(b"test")
    print(leafs)
    tree = []
    for i in range(0, len(leafs), 2):
        print(i)
        if not ((leafs[i] == '') & (leafs[i+1] == '')):
            print('one')
            left = leafs[i]
            right = leafs[i+1] if leafs[i+1] != '' else left
            preimage = bytes.fromhex(left + right)
            digest = hasher.hash_bytes(preimage)
            compressedDigest = Point.compress(digest).hex()
            tree.append(compressedDigest)
        else:
            print('two')
            tree.append('')

    if len(leafs) > 2:
        tree.extend(compute_merkle_tree(tree))

    return tree

def compute_full_merkle_tree(leafs):
    next_exponent_two = 2**math.ceil(math.log(len(leafs),2))
    leafs.extend(['' for _ in range(0, next_exponent_two-len(leafs))])
    leafs.extend(compute_full_merkle_tree_helper(leafs))
    return leafs

#test
#print(compute_full_merkle_tree(['000000000000000000096077576a25a456c71ec9dbc4199ccd6f7927ac346aff','00000000000000000001099e1a3416ca8b396ea983ebcc6a53f16be7cf5e5991', '000000000000000000045ffde9a4e9481cee2db487fbf267fb5b406d9391953f', '0000000000000000000c2a25d4cb3efa22187b97892fd9739d54b7cba6f33f3d', '0000000000000000000f7e22a81383aa0fbd5daa1256a42185a4b4e938c8d219']))
