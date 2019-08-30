from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def getBlock(i):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%("user27859F7V3Da7u5K", "1952IB39AaFJQzN"))
    block_hash = rpc_connection.getblockhash(i)
    return rpc_connection.getblock(block_hash)


def calculateNextTarget(i):
    current_block = getBlock(i)
    epoch_head_block = getBlock(i-2015)
    time_delta = int(current_block["time"])-int(epoch_head_block["time"])
    target_time_delta = 600 * 2016
    target = '00' + hex(int(int(current_block["bits"][2:] +
                            '00' * (int(current_block["bits"][:2], 16) - 3), 16) * time_delta / target_time_delta))[2:]
    target = '00' + hex(bitsToBigInt('1d00ffff'))[2:] if int(target, 16) > bitsToBigInt('1d00ffff') else target
    return target

def calculateNextTargetTest(i):
    current_block = getBlock(i)
    epoch_head_block = getBlock(i-2015)
    time_delta = int(current_block["time"])-int(epoch_head_block["time"])
    #print('Time delta: ' + str(time_delta))
    target_time_delta = 600 * 2016
    current_target = int(current_block["bits"][2:] + '00' * (int(current_block["bits"][:2], 16) - 3), 16)
    #print('Current target: ' + str(current_target))
    #print('Current target: ' + str(hex(current_target)))
    new_target = current_target * time_delta #/ target_time_delta
    #print('New target: ' + str(new_target))
    #print('New target: ' + str(targetToBits(hex(new_target)[2:])))
    #print('New target: ' + str(hex(new_target)))
    target = '00' + hex(int(bitsToBigInt(current_block["bits"]) * time_delta / target_time_delta))[2:]
    target = bitsToBigInt('1d00ffff') if int(target, 16) < bitsToBigInt('1d00ffff') else target
    return target


def targetToBits(target):
    return hex(int(len(target) / 2)) + target[:6]


def bitsToBigInt(bits):
    return int(bits[2:] + '00' * (int(bits[:2], 16) - 3), 16)


def main():
    target = calculateNextTarget(32255)
    #target = calculateNextTarget(2015)
    target_time_delta = 600 * 2016
    print('Calculated Target: \t\t\t\t' + str(target))
    print('Calculated Target bits: \t\t' + str(targetToBits(target)))

    print('Calculated Target Extended: \t' + str(int(target, 16)))

    actualTarget = bitsToBigInt(getBlock(32256)["bits"])
    actualTargetExtended = actualTarget * target_time_delta
    print('Actual Target: \t\t\t\t\t' + str(actualTarget))
    print('Actual Target Extended: \t\t' + str(actualTargetExtended))



if __name__ == "__main__":
    main()
