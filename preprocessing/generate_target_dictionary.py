for i in range(23, 32):
    padding = (i-19)*8
    print('if pack128([...[0; 120], ...bits[0..8]]) == ' + str(i) +
          ' then pack128([...[0; ' + str(128 - padding - 24) + '], ...bits[8..32], ...[0; ' + str(padding) + ']]) else \\')