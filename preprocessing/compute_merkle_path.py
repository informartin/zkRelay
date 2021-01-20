import json
from .create_input import hexToEightByteHexArray
from .create_input import hexToDecimalZokratesInput

def compute_merkle_path(tree, element):
    i = tree.index(element)
    path = []
    direction = []
    while i > 0:
        if i % 2 == 0:
            path.append(tree[i-1])
            direction.append(0)
        else:
            if tree[i+1] != '':
                path.append(tree[i+1])
            else:
                path.append(tree[i])
            direction.append(1)
        i = int((i-1)/2)

    return [path, direction]

def get_proof_input(tree, element, header):
    path = compute_merkle_path(tree, element)
    return json.dumps([hexToDecimalZokratesInput(header), [hexToEightByteHexArray(str(element)) for element in path[0]], [str(element) for element in path[1]]]).replace('"', '\\"')
