def generate_target():
    for i in range(23, 32):
        padding = (i-19)*8
        print('if pack128([...[0; 120], ...bits[0..8]]) == ' + str(i) +
              ' then pack128([...[0; ' + str(128 - padding - 24) + '], ...bits[8..32], ...[0; ' + str(padding) + ']]) else \\')


def generate_max_variance():
    for i in range(1,33):
        print('result = if length == ' + str(i) + ' then pack128([...[0; ' + str(128-4*i) + '], ...[1; ' + str(i*4) + ']]) else result fi')


def generate_bit_hex_map():
    bits = 0
    for i in range(1, 33):
        print('result = if bit_length > ' + str(bits) + ' then ' + str(i) + ' else result fi')
        bits = bits + 4
