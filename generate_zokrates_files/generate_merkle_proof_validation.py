import math


def generate_create_hash():
    return '''
def create_hash(field[5] preimage) -> (field[256]):
	a = unpack128(preimage[0])
	b = unpack128(preimage[1])
	c = unpack128(preimage[2])
	d = unpack128(preimage[3])
	e = unpack128(preimage[4])

	field[256] preimage1 = [...a, ...b]
    field[256] preimage2 = [...c, ...d]
    field[256] preimage3 = [...[...e, 1], ...[0; 127]]
    field[256] dummy = [...[0; 246], ...[1, 0, 1, 0, 0, 0, 0, 0, 0, 0]] //second array indicates length of preimage = 640bit

    intermediary = sha256for1024(preimage1, preimage2, preimage3, dummy)
    
	return sha256only(intermediary)

    '''


def generate_merkle_proof_validation_code(number_leafs):
    layers = math.ceil(math.log(number_leafs, 2))
    code = []

    code.append('import "hashes/pedersen/512bit.zok" as pedersenhash')
    code.append('import "utils/pack/pack128.zok" as pack128\n')
    code.append('import "utils/pack/unpack128.zok" as unpack128\n')
    code.append('import "hashes/sha256/1024bit.zok" as sha256for1024\n')
    code.append('import "../sha256only.zok" as sha256only')

    code.append(generate_create_hash())

    code.append('def main(field[5] preimage, private field[{layers}][256] path, private field[{layers}] lr) -> (field[4]):'.format(layers=layers))
    code.append('\tunpacked_proof_header = create_hash(preimage)')
    code.append('\tfield[256] layer0 = if lr[0] == 0 then pedersenhash([...path[0], ...unpacked_proof_header]) else pedersenhash([...unpacked_proof_header, ...path[0]]) fi')

    for i in range(1, layers):
        code.append('\tfield[256] layer{i} = if lr[{i}] == 0 then pedersenhash([...path[{i}], ...layer{preceeding}]) else pedersenhash([...layer{preceeding}, ...path[{i}]]) fi'.format(i=i, preceeding= i-1))

    code.append('\tres0 = pack128(layer{layers}[0..128])'.format(layers=layers-1))
    code.append('\tres1 = pack128(layer{layers}[128..256])'.format(layers=layers-1))

    code.append('\tfield[2] proof_header = [pack128(unpacked_proof_header[0..128]), pack128(unpacked_proof_header[128..256])]')
    code.append('\treturn [...proof_header, res0, res1]')

    return '\n'.join(code)
