import math


def generate_create_hash():
    return '''
def create_hash(bool[640] preimage) -> (bool[256]):
	bool[256] intermediary = sha256for1024(preimage[0..256], preimage[256..512], [...preimage[512..640], true, ...[false; 127]], [...[false; 246], true, false, true, ...[false; 7]])
    return sha256only(intermediary)

    '''


def generate_merkle_proof_validation_code(number_leafs):
    layers = math.ceil(math.log(number_leafs, 2))
    code = []
    code.append('import "hashes/pedersen/512bit.zok" as pedersenhash')
    code.append('import "hashes/sha256/embed/1024bit.zok" as sha256for1024\n')
    code.append('import "hashes/sha256/embed/256bitPadded.zok" as sha256only\n')
    code.append('import "utils/pack/bool/pack128.zok" as pack_128_bool_to_field\n')
    code.append('import "utils/pack/u32/pack128.zok" as pack_u32_4_to_field\n')
    code.append('import "utils/pack/bool/unpack128.zok" as unpack_field_to_128_bool\n')
    code.append('import "utils/casts/bool_128_to_u32_4.zok" as bool_128_to_u32_4\n')


    code.append(generate_create_hash())
    code.append('def main(field[5] preimage_field, private u32[{layers}][8] path, private field[{layers}] lr) -> (field[2][2]):'.format(layers=layers))
    code.append('\tbool[640] preimage = [...unpack_field_to_128_bool(preimage_field[0]), ...unpack_field_to_128_bool(preimage_field[1]), ...unpack_field_to_128_bool(preimage_field[2]), ...unpack_field_to_128_bool(preimage_field[3]), ...unpack_field_to_128_bool(preimage_field[4])]')
    code.append('\tbool[256] proof_header = create_hash(preimage)')
    code.append('\tu32[8] layer0 = if lr[0] == 0 then pedersenhash([...path[0], ...bool_128_to_u32_4(proof_header[0..128]), ...bool_128_to_u32_4(proof_header[128..256])]) else pedersenhash([...bool_128_to_u32_4(proof_header[0..128]), ...bool_128_to_u32_4(proof_header[128..256]), ...path[0]]) fi')

    for i in range(1, layers):
        code.append('\tu32[8] layer{i} = if lr[{i}] == 0 then pedersenhash([...path[{i}], ...layer{preceeding}]) else pedersenhash([...layer{preceeding}, ...path[{i}]]) fi'.format(i=i, preceeding= i-1))

    code.append('\treturn [[pack_128_bool_to_field(proof_header[0..128]), pack_128_bool_to_field(proof_header[128..256])], [pack_u32_4_to_field(layer{layers}[0..4]), pack_u32_4_to_field(layer{layers}[4..8])]]'.format(layers=layers-1))

    return '\n'.join(code)
