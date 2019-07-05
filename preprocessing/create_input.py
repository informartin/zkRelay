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


def getBlocksInRange(i, j):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%("user27859F7V3Da7u5K", "1952IB39AaFJQzN"))
    commands = [["getblockhash", height] for height in range(i, j)]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([["getblock", h] for h in block_hashes])
    return blocks


def hexToDecimalZokratesInput(input):
    preimage = bytes.fromhex(input)
    bitarray = BitArray(bytes=preimage)
    return [int(i, 2) for i in splitStringFromBack(bitarray.bin, 128)]


def createZokratesInputFromBlock(block):
    version = littleEndian(block['versionHex'])
    little_endian_previousHash = littleEndian(block['previousblockhash'])
    little_endian_merkleRoot = littleEndian(block['merkleroot'])
    little_endian_time = littleEndian(hex(block['time'])[2:])
    little_endian_difficultyBits = littleEndian(block['bits'])
    little_endian_nonce = littleEndian(hex(block['nonce'])[2:])
    little_endian_nonce = '0' + little_endian_nonce if len(little_endian_nonce) % 2 != 0 else little_endian_nonce

    header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce

    return hexToDecimalZokratesInput(header)

first_block = 579379
last_block = 579383
blocks = getBlocksInRange(first_block, last_block+1)

print(getBlocksInRange(first_block-1,first_block)[0]["hash"])

prior_blockhash = GENESIS_BLOCK_HASH if first_block == 1 else getBlocksInRange(first_block-1,first_block)[0]["hash"]
prior_block_zokrates_input = hexToDecimalZokratesInput(littleEndian(prior_blockhash))
intermediate_zokrates_blocks = [createZokratesInputFromBlock(block) for block in blocks[0:4]]
intermediate_zokrates_blocks = [item for sublist in intermediate_zokrates_blocks for item in sublist] #flatten
final_zokrates_block = createZokratesInputFromBlock(blocks[4])

print('zokrates input: ' + str([*prior_block_zokrates_input, *intermediate_zokrates_blocks, *final_zokrates_block]))
