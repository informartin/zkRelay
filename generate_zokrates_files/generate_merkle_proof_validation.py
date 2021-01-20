import math


def generate_create_hash():
    return '''
def create_hash(u32[20] preimage) -> (u32[8]):
	u32[8] intermediary = sha256for1024(preimage[0..8], preimage[8..16], [...preimage[16..20], 0x80000000, ...[0x00000000; 3]], [...[0x00000000; 7], 0x00000280])
    return sha256only(intermediary)

    '''


def generate_merkle_proof_validation_code(number_leafs):
    layers = math.ceil(math.log(number_leafs, 2))
    code = []

    code.append('import "hashes/pedersen/512bit.zok" as pedersenhash')
    code.append('import "hashes/sha256/1024bit.zok" as sha256for1024\n')
    code.append('import "hashes/sha256/256bitPadded.zok" as sha256only\n')
    code.append('import "utils/pack/u32/pack128.zok" as pack_4_u32_to_field\n')
    code.append('import "utils/pack/u32/unpack128.zok" as unpack_field_to_4_u32\n')


    code.append(generate_create_hash())
    code.append('def main(field[5] preimage_field, private u32[{layers}][8] path, private field[{layers}] lr) -> (field[2][2]):'.format(layers=layers))
    code.append('\tu32[20] preimage = [...unpack_field_to_4_u32(preimage_field[0]), ...unpack_field_to_4_u32(preimage_field[1]), ...unpack_field_to_4_u32(preimage_field[2]), ...unpack_field_to_4_u32(preimage_field[3]), ...unpack_field_to_4_u32(preimage_field[4])]')
    code.append('\tu32[8] proof_header = create_hash(preimage)')
    code.append('\tu32[8] layer0 = if lr[0] == 0 then pedersenhash([...path[0], ...proof_header]) else pedersenhash([...proof_header, ...path[0]]) fi')

    for i in range(1, layers):
        code.append('\tu32[8] layer{i} = if lr[{i}] == 0 then pedersenhash([...path[{i}], ...layer{preceeding}]) else pedersenhash([...layer{preceeding}, ...path[{i}]]) fi'.format(i=i, preceeding= i-1))

    code.append('\treturn [[pack_4_u32_to_field(proof_header[0..4]), pack_4_u32_to_field(proof_header[4..8])], [pack_4_u32_to_field(layer{layers}[0..4]), pack_4_u32_to_field(layer{layers}[4..8])]]'.format(layers=layers-1))

    return '\n'.join(code)
