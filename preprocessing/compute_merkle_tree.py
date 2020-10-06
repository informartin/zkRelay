from zokrates_pycrypto.babyjubjub import Point
from zokrates_pycrypto.gadgets.pedersenHasher import PedersenHasher
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
    tree = []
    for i in range(0, len(leafs), 2):
        if not ((leafs[i] == '') & (leafs[i+1] == '')):
            left = leafs[i]
            right = leafs[i+1] if leafs[i+1] != '' else left
            preimage = bytes.fromhex(left + right)
            digest = hasher.hash_bytes(preimage)
            compressedDigest = Point.compress(digest).hex()
            tree.append(compressedDigest)
        else:
            tree.append('')

    if len(leafs) > 2:
        tree[:0] = compute_full_merkle_tree_helper(tree)

    return tree

def compute_full_merkle_tree(leafs):
    # fill tree
    next_exponent_two = 2**math.ceil(math.log(len(leafs),2))
    leafs.extend(['' for _ in range(0, next_exponent_two-len(leafs))])
    leafs[:0] = compute_full_merkle_tree_helper(leafs)
    return leafs
