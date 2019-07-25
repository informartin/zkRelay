def generate_block_validation_call(amount):
    for i in range(2, amount):
        print('block' + str(i) + ' = validate_block_header(block' + str(i-1) + '[1..3], intermediate_blocks[' + str((i - 1) * 5) + '..' + str(i * 5) + '])')
        print('result = if block' + str(i) + '[0] == 0 || result == 0 then 0 else 1 fi')



'''    
block2 = validate_block_header(block1[1..3], intermediate_blocks[5..10])
result = if block2[0] == 0 || result == 0 then 0 else 1 fi
'''

generate_block_validation_call(2016)