import math


def generate_merkle_proof_validation_code(number_leafs):
    layers = math.ceil(math.log(number_leafs, 2))
    code = []

    code.append('import "hashes/pedersen/512bit.zok" as pedersenhash')
    code.append('import "utils/pack/pack128.zok" as pack128\n')
    code.append('import "utils/pack/unpack128.zok" as unpack128\n')

    code.append('def main(field[2] proof_header, private field[{layers}][256] path, private field[{layers}] lr) -> (field[2]):'.format(layers=layers))
    code.append('\tfield[256] unpacked_proof_header = [...unpack128(proof_header[0]), ...unpack128(proof_header[1])]')
    code.append('\tfield[256] layer0 = if lr[0] == 0 then pedersenhash([...path[0], ...unpacked_proof_header]) else pedersenhash([...unpacked_proof_header, ...path[0]]) fi')

    for i in range(1, layers):
        code.append('\tfield[256] layer{i} = if lr[{i}] == 0 then pedersenhash([...path[{i}], ...layer{preceeding}]) else pedersenhash([...layer{preceeding}, ...path[{i}]]) fi'.format(i=i, preceeding= i-1))

    code.append('\tres0 = pack128(layer{layers}[0..128])'.format(layers=layers-1))
    code.append('\tres1 = pack128(layer{layers}[128..256])'.format(layers=layers-1))

    code.append('\treturn [res0, res1]')

    return '\n'.join(code)
