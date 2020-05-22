from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from bitstring import BitArray

GENESIS_BLOCK_HASH = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'


def splitStringFromBack(word, border):
    reverse_word = (word[::-1])
    split_reverse = [reverse_word[i:i+border] for i in range(0, len(reverse_word), border)]
    return list(reversed([i[::-1] for i in split_reverse]))


def littleEndian(string):
    splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
    splited.reverse()
    return "".join(splited)


def getCredentials():
    with open('preprocessing/pw') as fp:
    	user = fp.readline()[:-1]
    	password = fp.readline()[:-1]
    return user, password


def getBlockHeadersInRange(i, j):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%getCredentials())
    commands = [["getblockhash", height] for height in range(i, j)]
    block_hashes = rpc_connection.batch_(commands)
    return block_hashes


def getBlocksInRange(i, j):
    block_hashes = getBlockHeadersInRange(i, j)
    blocks = rpc_connection.batch_([["getblock", h] for h in block_hashes])
    return blocks


def hexToDecimalZokratesInput(input):
    preimage = bytes.fromhex(input)
    bitarray = BitArray(bytes=preimage)
    return [int(i, 2) for i in splitStringFromBack(bitarray.bin, 128)]


def hexToBinaryZokratesInput(input):
    preimage = bytes.fromhex(input)
    bitarray = BitArray(bytes=preimage)
    return " ".join(bitarray.bin)


def createZokratesInputFromBlock(block):
    version = littleEndian(block['versionHex'])
    little_endian_previousHash = littleEndian(block['previousblockhash']) if block['height'] > 0 else 64 * '0'
    little_endian_merkleRoot = littleEndian(block['merkleroot'])
    little_endian_time = littleEndian(hex(block['time'])[2:])
    little_endian_difficultyBits = littleEndian(block['bits'])
    nonce = hex(block['nonce'])[2:]
    nonce = '0' * (8 - len(nonce)) + nonce #ensure nonce is 4 bytes long
    little_endian_nonce = littleEndian(nonce)

    header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce

    return header


def generateZokratesInputFromBlockLegacy(first_block, amount):
    last_block = first_block + amount - 1
    blocks = getBlocksInRange(first_block, last_block+1)

    prior_blockhash = GENESIS_BLOCK_HASH if first_block == 1 else getBlocksInRange(first_block-1,first_block)[0]["hash"]
    prior_block_zokrates_input = hexToDecimalZokratesInput(littleEndian(prior_blockhash))
    intermediate_zokrates_blocks = [createZokratesInputFromBlock(block) for block in blocks[0:amount - 1]]
    intermediate_zokrates_blocks = [item for sublist in intermediate_zokrates_blocks for item in sublist] #flatten
    final_zokrates_block = createZokratesInputFromBlock(blocks[amount - 1])

    print(str([*prior_block_zokrates_input, *intermediate_zokrates_blocks, *final_zokrates_block])
          .replace(',','')
          .replace('[','')
          .replace(']',''))


def generateZokratesInputFromBlock(first_block, amount):
    last_block = first_block + amount
    blocks = getBlocksInRange(first_block, last_block)

    #prior_blockhash = GENESIS_BLOCK_HASH if first_block == 1 else getBlocksInRange(first_block-1,first_block)[0]["hash"]
    #prior_block_zokrates_input = hexToDecimalZokratesInput(littleEndian(prior_blockhash))
    epoch_header_block_number = first_block if (first_block+1) % 2016 == 0 else first_block - (first_block % 2016)
    epoch_head = getBlocksInRange(epoch_header_block_number, epoch_header_block_number+1) \
        if first_block >= 2016 else getBlocksInRange(0, 1)
    epoch_head = hexToDecimalZokratesInput(createZokratesInputFromBlock(epoch_head[0]))
    #list(map(lambda x: print(x['height']), blocks[0:len(blocks)-1]))
    #print(blocks[len(blocks)-1]['height'])
    prev_block_hash = hexToDecimalZokratesInput(littleEndian(getBlocksInRange(first_block-1,first_block)[0]["hash"]))
    intermediate_zokrates_blocks = [hexToBinaryZokratesInput(createZokratesInputFromBlock(block)) for block in blocks[0:len(blocks)-1]]
    #intermediate_zokrates_blocks = [item for sublist in intermediate_zokrates_blocks for item in sublist] #flatten
    final_zokrates_block = hexToDecimalZokratesInput(createZokratesInputFromBlock(blocks[len(blocks)-1]))
    return str([epoch_head[4], *prev_block_hash, *intermediate_zokrates_blocks, *final_zokrates_block]).replace(',','').replace('[','').replace(']','').replace('\'','')


def generateZokratesInputForBlocks(blocks):
    blocks = [getBlocksInRange(i, i+1) for i in blocks]
    blocks = [item for sublist in blocks for item in sublist] #flatten
    zokrates_blocks = [createZokratesInputFromBlock(block) for block in blocks[0:len(blocks)]]
    print(str(zokrates_blocks).replace(',','').replace('[','').replace(']',''))


def generateZokratesInputForMerkleProof(first_block, amount):
    last_block = first_block + amount - 1
    block_hashes = [littleEndian(header) for header in getBlockHeadersInRange(first_block, last_block+1)]
    joined_blocks = ''.join(block_hashes)
    return hexToBinaryZokratesInput(joined_blocks)
