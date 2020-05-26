from create_input import hexToBinaryZokratesInput

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

def get_proof_input(tree, element):
    path = compute_merkle_path(tree, element)
    return hexToBinaryZokratesInput(element) + ' ' + hexToBinaryZokratesInput(''.join(path[0])) + ' ' + ' '.join([str(element) for element in path[1]])
