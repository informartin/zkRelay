
import math


def generate_compute_root(number_leafs):
    if number_leafs > 2:
        output = '\tu32[{len}][8] layer{layer} = [\n'.format(len=math.ceil(number_leafs/2), layer=(math.ceil(math.log(number_leafs,2))-1))
    else:
        output = '\tu32[8] layer{layer} = '.format(layer=(math.ceil(math.log(number_leafs,2))-1))
    for i in range(0, number_leafs-2, 2):
        output = output + '\t\tpedersenhash([...layer{layer}[{a}], ...layer{layer}[{b}]]),\n'.format(a=i, b=i+1, layer=math.ceil(math.log(number_leafs,2)))
    output = output + '\t\tpedersenhash([...layer{layer}[{a}], ...layer{layer}[{b}]])\n'.format(a=number_leafs-2 if number_leafs % 2 == 0 else number_leafs-1, b=number_leafs-1, layer=math.ceil(math.log(number_leafs,2)))
    if number_leafs > 2:
        output = output + '\t]\n'

    if number_leafs > 2:
        output = output + generate_compute_root(math.ceil(number_leafs/2))

    return output


def generate_root_code(number_leafs):
    output = ('import "hashes/pedersen/512bit.zok" as pedersenhash\n' +
        'def main(u32[{number_leafs}][8] layer{layer}) -> (u32[8]):\n'.format(number_leafs=number_leafs,layer=math.ceil(math.log(number_leafs,2))) +
        generate_compute_root(number_leafs) +
        '\treturn layer0')
    return output