import hashlib
from bitstring import BitArray

#convert into little endian format
def littleEndian(string):
    splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
    splited.reverse()
    return "".join(splited)

def splitStringFromBack(word, border):
    reverse_word = (word[::-1])
    split_reverse = [reverse_word[i:i+border] for i in range(0, len(reverse_word), border)]
    return list(reversed([i[::-1] for i in split_reverse]))

previousblockhash = "00000000000000000009ce5ffa68f23604a8bca42802a32f0b494e0f329ed74e"
merkleroot = "278acfb9209cd2ba2a8776e506567f710550020a6009e73fc7e7bb61f4b64dd1"
time = hex(1559748012)[2:]
#difficulty = calcDiff(7459680720542.296)
bits = "1725bb76"
nonce = hex(1327516660)[2:]
hash = "00000000000000000008df1d19378b05d136cbc56453f3fa87bc0898b4c96e9a"

version = littleEndian("20c00000")

little_endian_previousHash = littleEndian(previousblockhash)
little_endian_merkleRoot = littleEndian(merkleroot)
little_endian_time = littleEndian(time)
little_endian_difficultyBits = littleEndian(bits)
little_endian_nonce = littleEndian(nonce)

header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce

preimage = bytes.fromhex(header)
bitarray = BitArray(bytes=preimage)
print('header: ' + header)
print('preimage: ' + str(preimage))
print('binary header: ' + bitarray.bin) #binary representation of pre-image
print('zokrates decimal input: ' + str([int(i, 2) for i in splitStringFromBack(bitarray.bin, 128)]))


#hash = hashlib.sha256(preimage).hexdigest() #compute hash
hash = hashlib.sha256(hashlib.sha256(preimage).digest()).hexdigest() #compute hash
print('computed hash: 0x' + hash)
a = 205276355077767745232354107659563775697
b = 7368986764737877624891463484722642944
hexa = hex(a)
hexb = hex(b)[2:] if len(str(a)) == len(str(b)) else '0' + hex(b)[2:] #pad with a 0 in front if length is smaller

print('zokrates hash: ' + hexa + hexb)
