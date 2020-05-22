from create_input import hexToBinaryZokratesInput

def compute_merkle_path(tree, element):
    i = tree.index(element)
    path = []
    direction = []
    while i > 0:
        if i % 2 == 0:
            path.append(tree[i-1])
            direction.append(0)
        else:
            if tree[i+1] != '':
                path.append(tree[i+1])
            else:
                path.append(tree[i])
            direction.append(1)
        i = int((i-1)/2)

    return [path, direction]

def get_proof_input(tree, element):
    path = compute_merkle_path(tree, element)
    return hexToBinaryZokratesInput(element) + ' ' + hexToBinaryZokratesInput(''.join(path[0])) + ' ' + ' '.join([str(element) for element in path[1]])

#print(compute_merkle_path(['9efde78a321ecc00c95a5215395086c63a3ab7c0afdad6b08839673456a2e50e', 'a4d2d79083a55d9c42dfac6a96597f76973d354eb84270c9827a2312af8c0e61', '0217dee9b57482f4a76271a7032a61827f5df0e58171fd286eadbbdcb94255eb', '17ecbf65c0001a812504efa51bb2bb444dfbc41aedb96241093d710d8c7c60af', '1225d53a13827e0a2d8506bf9c9fb0e2b4817d7a80d90c83a195b72ce4be39ea', '96b1c64dd4b2df80648cfe18768db54c442310f4bddb7335b8ec29c0e32ecced', '', '00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048', '000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd', '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449', '000000004ebadb55ee9096c9a2f8880e09da59c0d68b1c228da88e48844a1485', '000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc', '', '', ''], '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449'))

print(get_proof_input(['9efde78a321ecc00c95a5215395086c63a3ab7c0afdad6b08839673456a2e50e', 'a4d2d79083a55d9c42dfac6a96597f76973d354eb84270c9827a2312af8c0e61', '0217dee9b57482f4a76271a7032a61827f5df0e58171fd286eadbbdcb94255eb', '17ecbf65c0001a812504efa51bb2bb444dfbc41aedb96241093d710d8c7c60af', '1225d53a13827e0a2d8506bf9c9fb0e2b4817d7a80d90c83a195b72ce4be39ea', '96b1c64dd4b2df80648cfe18768db54c442310f4bddb7335b8ec29c0e32ecced', '', '00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048', '000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd', '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449', '000000004ebadb55ee9096c9a2f8880e09da59c0d68b1c228da88e48844a1485', '000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc', '', '', ''], '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449'))
