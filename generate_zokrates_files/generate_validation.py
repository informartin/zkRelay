def generate_validation_code(n_blocks):
    static_code = """import "utils/pack/pack128.zok" as pack128
import "utils/pack/unpack128.zok" as unpack128
import "hashes/sha256/1024bit.zok" as sha256for1024
import "./sha256only.zok" as sha256only
import "./getHexLength.zok" as getHexLength
import "./compute_merkle_root.zok" as compute_merkle_root

def toBigEndian(field[32] value) -> (field[32]):
    return [
            ...value[24..32],
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]]

def toBigEndian(field[24] value) -> (field[24]):
    return [
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]]

def toBigEndian(field[128] value) -> (field[128]):
    return [
            ...value[120..128],
            ...value[112..120],
            ...value[104..112],
            ...value[96..104],
            ...value[88..96],
            ...value[80..88],
            ...value[72..80],
            ...value[64..72],
            ...value[56..64],
            ...value[48..56],
            ...value[40..48],
            ...value[32..40],
            ...value[24..32],
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]]

def packMaxVariance(field length) -> (field):
    field result = 0
    result = if length == 1 then pack128([...[0; 124], ...[1; 4]]) else result fi
    result = if length == 2 then pack128([...[0; 120], ...[1; 8]]) else result fi
    result = if length == 3 then pack128([...[0; 116], ...[1; 12]]) else result fi
    result = if length == 4 then pack128([...[0; 112], ...[1; 16]]) else result fi
    result = if length == 5 then pack128([...[0; 108], ...[1; 20]]) else result fi
    result = if length == 6 then pack128([...[0; 104], ...[1; 24]]) else result fi
    result = if length == 7 then pack128([...[0; 100], ...[1; 28]]) else result fi
    result = if length == 8 then pack128([...[0; 96], ...[1; 32]]) else result fi
    result = if length == 9 then pack128([...[0; 92], ...[1; 36]]) else result fi
    result = if length == 10 then pack128([...[0; 88], ...[1; 40]]) else result fi
    result = if length == 11 then pack128([...[0; 84], ...[1; 44]]) else result fi
    result = if length == 12 then pack128([...[0; 80], ...[1; 48]]) else result fi
    result = if length == 13 then pack128([...[0; 76], ...[1; 52]]) else result fi
    result = if length == 14 then pack128([...[0; 72], ...[1; 56]]) else result fi
    result = if length == 15 then pack128([...[0; 68], ...[1; 60]]) else result fi
    result = if length == 16 then pack128([...[0; 64], ...[1; 64]]) else result fi
    result = if length == 17 then pack128([...[0; 60], ...[1; 68]]) else result fi
    result = if length == 18 then pack128([...[0; 56], ...[1; 72]]) else result fi
    result = if length == 19 then pack128([...[0; 52], ...[1; 76]]) else result fi
    result = if length == 20 then pack128([...[0; 48], ...[1; 80]]) else result fi
    result = if length == 21 then pack128([...[0; 44], ...[1; 84]]) else result fi
    result = if length == 22 then pack128([...[0; 40], ...[1; 88]]) else result fi
    result = if length == 23 then pack128([...[0; 36], ...[1; 92]]) else result fi
    result = if length == 24 then pack128([...[0; 32], ...[1; 96]]) else result fi
    result = if length == 25 then pack128([...[0; 28], ...[1; 100]]) else result fi
    result = if length == 26 then pack128([...[0; 24], ...[1; 104]]) else result fi
    result = if length == 27 then pack128([...[0; 20], ...[1; 108]]) else result fi
    result = if length == 28 then pack128([...[0; 16], ...[1; 112]]) else result fi
    result = if length == 29 then pack128([...[0; 12], ...[1; 116]]) else result fi
    result = if length == 30 then pack128([...[0; 8], ...[1; 120]]) else result fi
    result = if length == 31 then pack128([...[0; 4], ...[1; 124]]) else result fi
    result = if length == 32 then pack128([1; 128]) else result fi
return result

def packTarget(field[32] bits) -> (field):
    field result = \\
    if pack128([...[0; 120], ...bits[0..8]]) == 23 then pack128([...[0; 72], ...bits[8..32], ...[0; 32]]) else \\
      if pack128([...[0; 120], ...bits[0..8]]) == 24 then pack128([...[0; 64], ...bits[8..32], ...[0; 40]]) else \\
        if pack128([...[0; 120], ...bits[0..8]]) == 25 then pack128([...[0; 56], ...bits[8..32], ...[0; 48]]) else \\
          if pack128([...[0; 120], ...bits[0..8]]) == 26 then pack128([...[0; 48], ...bits[8..32], ...[0; 56]]) else \\
            if pack128([...[0; 120], ...bits[0..8]]) == 27 then pack128([...[0; 40], ...bits[8..32], ...[0; 64]]) else \\
              if pack128([...[0; 120], ...bits[0..8]]) == 28 then pack128([...[0; 32], ...bits[8..32], ...[0; 72]]) else \\
                if pack128([...[0; 120], ...bits[0..8]]) == 29 then pack128([...[0; 24], ...bits[8..32], ...[0; 80]]) else \\
                  if pack128([...[0; 120], ...bits[0..8]]) == 30 then pack128([...[0; 16], ...bits[8..32], ...[0; 88]]) else \\
                    if pack128([...[0; 120], ...bits[0..8]]) == 31 then pack128([...[0; 8], ...bits[8..32], ...[0; 96]]) else \\
                    pack128([0; 128]) fi \\
                  fi \\
                fi \\
              fi \\
            fi \\
          fi \\
        fi \\
      fi \\
    fi
return result

def get_bit_length_bits(field[24] bits) -> (field):
    field result = 0
    for field i in 0..24 do
        result = if (result == 0) && (bits[i] == 1) then 24-i else result fi
    endfor
return result

def get_hex_length_bits(field[24] bits) -> (field):
    field bit_length = get_bit_length_bits(bits)
    field result = 0
    result = if bit_length > 0 then 1 else result fi
    result = if bit_length > 4 then 2 else result fi
    result = if bit_length > 8 then 3 else result fi
    result = if bit_length > 12 then 4 else result fi
    result = if bit_length > 16 then 5 else result fi
    result = if bit_length > 20 then 6 else result fi
return result

// call with last field of block array
def validate_target(field epoch_head, field epoch_tail, field next_epoch_head) -> (field[2]):
    field[128] epoch_head_unpacked = unpack128(epoch_head)
    field[128] epoch_tail_unpacked = unpack128(epoch_tail)
    field[128] next_epoch_head_unpacked = unpack128(next_epoch_head)
    field time_head = pack128([...[0; 96], ...toBigEndian(epoch_head_unpacked[32..64])])
    field time_tail = pack128([...[0; 96], ...toBigEndian(epoch_tail_unpacked[32..64])])

    field current_target = packTarget(toBigEndian(epoch_head_unpacked[64..96]))
    field time_delta = time_tail - time_head
    field target_time_delta = 1209600 // 2016 * 600 (time interval of 10 minutes)

    field target = current_target * time_delta // target_time_delta

    field encoded_target = packTarget(toBigEndian(next_epoch_head_unpacked[64..96]))
    field encoded_target_extended = encoded_target * target_time_delta

    // The encoding of targets uses a floor function, the comparison of a calculated target may therefore fail
    // Therefore, a maximum variance is calculated that is one hex digit in the encoding
    field maxVariance = packMaxVariance(getHexLength(target)-get_hex_length_bits(toBigEndian(next_epoch_head_unpacked[64..88])))
    // int('ffff' + 10 * '00', 16) * 2016 * 600 = 95832923060582736897701037735936000
    target = if target > 95832923060582736897701037735936000 then 95832923060582736897701037735936000 else target fi
    field delta = target - encoded_target_extended
    delta = if target >= encoded_target_extended then delta else maxVariance + 1 fi
    field valid = if delta <= maxVariance then 1 else 0 fi
    //field valid = if (37202390668975264121251936602161152-81015268229227203625641762304819200) < 1267650600228229401496703205375 then 1 else 0 fi
return [valid, current_target]

def hash_block_header(field[5] preimage) -> (field[2]):
    field[128] a = unpack128(preimage[0])
    field[128] b = unpack128(preimage[1])
    field[128] c = unpack128(preimage[2])
    field[128] d = unpack128(preimage[3])
    field[128] e = unpack128(preimage[4])

    field[256] preimage1 = [...a, ...b]
    field[256] preimage2 = [...c, ...d]
    field[256] preimage3 = [...[...e, 1], ...[0; 127]]
    field[256] dummy = [...[0; 246], ...[1, 0, 1, 0, 0, 0, 0, 0, 0, 0]] //second array indicates length of preimage = 640bit

    field[256] intermediary = sha256for1024(preimage1, preimage2, preimage3, dummy)

    field[256] r = sha256only(intermediary)

    field res0 = pack128(r[0..128])
    field res1 = pack128(r[128..256])

return [res0, res1]


def validate_block_header(field reference_target, field[256] bin_prev_block_hash, field[5] preimage) -> (field[257]):
    a = unpack128(preimage[0])
	b = unpack128(preimage[1])
	c = unpack128(preimage[2])
	d = unpack128(preimage[3])
	e = unpack128(preimage[4])

    encoded_prev_block_hash1 = pack128([...a[32..128], ...b[0..32]])
    encoded_prev_block_hash2 = pack128([...b[32..128], ...c[0..32]])
    field[2] prev_block_hash = [pack128(bin_prev_block_hash[0..128]), pack128(bin_prev_block_hash[128..256])]
    field valid = if encoded_prev_block_hash1 == prev_block_hash[0] && encoded_prev_block_hash2 == prev_block_hash[1] \\
        then 1 else 0 fi

    // converting to big endian is not necessary here, as reference target is encoded little endian
    field current_target = pack128([...[0; 96], ...e[64..96]])
    valid = if valid == 1 && current_target == reference_target then 1 else 0 fi

    field[256] preimage1 = [...a, ...b]
    field[256] preimage2 = [...c, ...d]
    field[256] preimage3 = [...[...e, 1], ...[0; 127]]
    field[256] dummy = [...[0; 246], ...[1, 0, 1, 0, 0, 0, 0, 0, 0, 0]] //second array indicates length of preimage = 640bit

    intermediary = sha256for1024(preimage1, preimage2, preimage3, dummy)
    
    r = sha256only(intermediary)

    target = packTarget(toBigEndian(e[64..96]))

    valid = if valid == 1 && target > pack128(toBigEndian(r[128..256])) then 1 else 0 fi

return [valid, ...r]

"""
    main_block = []
    main_block.append("def main(field first_block_epoch, field[2] prev_block_hash, private field[{n_intermediate}][5] intermediate_blocks, field[5] final_block) -> (field[7]):".format(n_intermediate=(n_blocks-1)))
    main_block.append("""
    field[128] unpacked_raw_target = unpack128(first_block_epoch)
    // converting to big endian is not necessary here, as it is compared to a little endian encoding
    // it is not used for calculations
    field reference_target = pack128([...[0; 96], ...unpacked_raw_target[64..96]])
    field result = 1
    field[128] bin_prev_block_hash1 = unpack128(prev_block_hash[0])
    field[128] bin_prev_block_hash2 = unpack128(prev_block_hash[1])
    field[257] block1 = validate_block_header(reference_target, [...bin_prev_block_hash1, ...bin_prev_block_hash2], intermediate_blocks[0])
    result = if block1[0] == 0 || result == 0 then 0 else 1 fi""")

    blocks = []

    for i in range(1,n_blocks-1):
        main_block.append("""
    field[257] block{a} = validate_block_header(reference_target, block{b}[1..257], intermediate_blocks[{b}])
    result = if block{a}[0] == 0 || result == 0 then 0 else 1 fi""".format(a=i+1, b=i))
        blocks.append('block' + str(i) + '[1..257]')

    blocks.append('block' + str(n_blocks-1) + '[1..257]')
    blocks.append('block' + str(n_blocks) + '[1..257]')

    main_block.append("""
    field[128] e = unpack128(final_block[4]) //TODO: Clean up, dirty mirty
    field[257] block{n_final_block} = validate_block_header(pack128([...[0; 96], ...e[64..96]]), block{n_prev_block}[1..257], final_block)
    result = if block{n_final_block}[0] == 0 || result == 0 then 0 else 1 fi

    field[2] target_is_valid = validate_target(first_block_epoch, intermediate_blocks[{n_enc_target}][4], final_block[4])

    field[2] merkle_root = compute_merkle_root([{blocks}])
    field[2] final_block_hash = [pack128(block{n_final_block}[1..129]), pack128(block{n_final_block}[129..257])]

return [result, target_is_valid[0], ...final_block_hash, target_is_valid[1], ...merkle_root]""".format(n_final_block=n_blocks, n_prev_block=n_blocks-1, n_enc_target=n_blocks-2, blocks=','.join(blocks)))

    return static_code + "\n".join(main_block)
