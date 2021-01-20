def generate_validation_code(n_blocks):
    static_code = """import "EMBED/u32_to_bits" as u32_to_bits
import "EMBED/u32_from_bits" as u32_from_bits
import "utils/casts/u32_4_to_bool_128.zok" as u32_4_to_bool_128
import "utils/pack/u32/pack128.zok" as u32_4_to_field
import "utils/pack/bool/pack128.zok" as pack_128_bool_to_field
import "utils/pack/bool/unpack128.zok" as unpack_field_to_128_bool
import "utils/pack/u32/unpack128.zok" as unpack_field_to_4_u32
import "hashes/sha256/1024bit.zok" as sha256for1024
import "hashes/sha256/256bitPadded.zok" as sha256only
import "./getHexLength.zok" as getHexLength
import "./compute_merkle_root.zok" as compute_merkle_root
def toBigEndian(bool[32] value) -> (bool[32]):
    return [
            ...value[24..32],
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]]
def toBigEndian(bool[24] value) -> (bool[24]):
    return [
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]]
def toBigEndian(bool[128] value) -> (bool[128]):
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
    result = if length == 1 then pack_128_bool_to_field([...[false; 124], ...[true; 4]]) else result fi
    result = if length == 2 then pack_128_bool_to_field([...[false; 120], ...[true; 8]]) else result fi
    result = if length == 3 then pack_128_bool_to_field([...[false; 116], ...[true; 12]]) else result fi
    result = if length == 4 then pack_128_bool_to_field([...[false; 112], ...[true; 16]]) else result fi
    result = if length == 5 then pack_128_bool_to_field([...[false; 108], ...[true; 20]]) else result fi
    result = if length == 6 then pack_128_bool_to_field([...[false; 104], ...[true; 24]]) else result fi
    result = if length == 7 then pack_128_bool_to_field([...[false; 100], ...[true; 28]]) else result fi
    result = if length == 8 then pack_128_bool_to_field([...[false; 96], ...[true; 32]]) else result fi
    result = if length == 9 then pack_128_bool_to_field([...[false; 92], ...[true; 36]]) else result fi
    result = if length == 10 then pack_128_bool_to_field([...[false; 88], ...[true; 40]]) else result fi
    result = if length == 11 then pack_128_bool_to_field([...[false; 84], ...[true; 44]]) else result fi
    result = if length == 12 then pack_128_bool_to_field([...[false; 80], ...[true; 48]]) else result fi
    result = if length == 13 then pack_128_bool_to_field([...[false; 76], ...[true; 52]]) else result fi
    result = if length == 14 then pack_128_bool_to_field([...[false; 72], ...[true; 56]]) else result fi
    result = if length == 15 then pack_128_bool_to_field([...[false; 68], ...[true; 60]]) else result fi
    result = if length == 16 then pack_128_bool_to_field([...[false; 64], ...[true; 64]]) else result fi
    result = if length == 17 then pack_128_bool_to_field([...[false; 60], ...[true; 68]]) else result fi
    result = if length == 18 then pack_128_bool_to_field([...[false; 56], ...[true; 72]]) else result fi
    result = if length == 19 then pack_128_bool_to_field([...[false; 52], ...[true; 76]]) else result fi
    result = if length == 20 then pack_128_bool_to_field([...[false; 48], ...[true; 80]]) else result fi
    result = if length == 21 then pack_128_bool_to_field([...[false; 44], ...[true; 84]]) else result fi
    result = if length == 22 then pack_128_bool_to_field([...[false; 40], ...[true; 88]]) else result fi
    result = if length == 23 then pack_128_bool_to_field([...[false; 36], ...[true; 92]]) else result fi
    result = if length == 24 then pack_128_bool_to_field([...[false; 32], ...[true; 96]]) else result fi
    result = if length == 25 then pack_128_bool_to_field([...[false; 28], ...[true; 100]]) else result fi
    result = if length == 26 then pack_128_bool_to_field([...[false; 24], ...[true; 104]]) else result fi
    result = if length == 27 then pack_128_bool_to_field([...[false; 20], ...[true; 108]]) else result fi
    result = if length == 28 then pack_128_bool_to_field([...[false; 16], ...[true; 112]]) else result fi
    result = if length == 29 then pack_128_bool_to_field([...[false; 12], ...[true; 116]]) else result fi
    result = if length == 30 then pack_128_bool_to_field([...[false; 8], ...[true; 120]]) else result fi
    result = if length == 31 then pack_128_bool_to_field([...[false; 4], ...[true; 124]]) else result fi
    result = if length == 32 then pack_128_bool_to_field([true; 128]) else result fi
return result
def packTarget(bool[32] bits) -> (field):
    field result = \
    if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 23 then pack_128_bool_to_field([...[false; 72], ...bits[8..32], ...[false; 32]]) else \
      if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 24 then pack_128_bool_to_field([...[false; 64], ...bits[8..32], ...[false; 40]]) else \
        if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 25 then pack_128_bool_to_field([...[false; 56], ...bits[8..32], ...[false; 48]]) else \
          if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 26 then pack_128_bool_to_field([...[false; 48], ...bits[8..32], ...[false; 56]]) else \
            if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 27 then pack_128_bool_to_field([...[false; 40], ...bits[8..32], ...[false; 64]]) else \
              if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 28 then pack_128_bool_to_field([...[false; 32], ...bits[8..32], ...[false; 72]]) else \
                if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 29 then pack_128_bool_to_field([...[false; 24], ...bits[8..32], ...[false; 80]]) else \
                  if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 30 then pack_128_bool_to_field([...[false; 16], ...bits[8..32], ...[false; 88]]) else \
                    if pack_128_bool_to_field([...[false; 120], ...bits[0..8]]) == 31 then pack_128_bool_to_field([...[false; 8], ...bits[8..32], ...[false; 96]]) else \
                    pack_128_bool_to_field([false; 128]) fi \
                  fi \
                fi \
              fi \
            fi \
          fi \
        fi \
      fi \
    fi
return result
def get_bit_length_bits(bool[24] bits) -> (field):
    field result = 0
    for field i in 0..24 do
        result = if (result == 0) && (bits[i] == true) then 24-i else result fi
    endfor
return result
def get_hex_length_bits(bool[24] bits) -> (field):
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
def validate_target(field epoch_head, u32 epoch_tail, u32 next_epoch_head) -> (bool, field):
    bool[128] epoch_head_unpacked = unpack_field_to_128_bool(epoch_head)
// 
    bool[32] epoch_tail_unpacked = u32_to_bits(epoch_tail)
    bool[32] next_epoch_head_unpacked = u32_to_bits(next_epoch_head)
    field time_head = pack_128_bool_to_field([...[false; 96], ...toBigEndian(epoch_head_unpacked[32..64])])
    field time_tail = pack_128_bool_to_field([...[false; 96], ...toBigEndian(epoch_tail_unpacked)])
    field current_target = packTarget(toBigEndian(epoch_head_unpacked[64..96]))
    field time_delta = time_tail - time_head
    field target_time_delta = 1209600 // 2016 * 600 (time interval of 10 minutes)
    field target = current_target * time_delta // target_time_delta
    field encoded_target = packTarget(toBigEndian(next_epoch_head_unpacked))
    field encoded_target_extended = encoded_target * target_time_delta
    // The encoding of targets uses a floor function, the comparison of a calculated target may therefore fail
    // Therefore, a maximum variance is calculated that is one hex digit in the encoding
    field maxVariance = packMaxVariance(getHexLength(target)-get_hex_length_bits(toBigEndian(next_epoch_head_unpacked[0..24])))
    // int('ffff' + 10 * '00', 16) * 2016 * 600 = 95832923060582736897701037735936000
    target = if target > 95832923060582736897701037735936000 then 95832923060582736897701037735936000 else target fi
    field delta = target - encoded_target_extended
    delta = if target >= encoded_target_extended then delta else maxVariance + 1 fi
    bool valid = if delta <= maxVariance then true else false fi
return valid, current_target
def validate_block_header(u32 reference_target, u32[8] prev_block_hash, field[5] preimage_field) -> (u32[8]):
   u32[20] preimage = [...unpack_field_to_4_u32(preimage_field[0]), ...unpack_field_to_4_u32(preimage_field[1]), ...unpack_field_to_4_u32(preimage_field[2]), ...unpack_field_to_4_u32(preimage_field[3]), ...unpack_field_to_4_u32(preimage_field[4])]
	// preImage: [0] -> Block version, [1:8] -> prev_block_hash, [9:16] -> merkle root, [17:19] => time, target, nonce 
    assert(preimage[1] == prev_block_hash[0] && \\
            preimage[2] == prev_block_hash[1] && \\
            preimage[3] == prev_block_hash[2] && \\
            preimage[4] == prev_block_hash[3] && \\
            preimage[5] == prev_block_hash[4] && \\
            preimage[6] == prev_block_hash[5] && \\
            preimage[7] == prev_block_hash[6] && \\
            preimage[8] == prev_block_hash[7])
    // converting to big endian is not necessary here, as reference target is encoded little endian
    assert(preimage[18] == reference_target)
    u32[8] intermediary = sha256for1024(preimage[0..8], preimage[8..16], [...preimage[16..20], 0x80000000, ...[0x00000000; 3]], [...[0x00000000; 7], 0x00000280])
    u32[8] r = sha256only(intermediary)
    field target = packTarget(toBigEndian(u32_to_bits(preimage[18])))
    assert(target > pack_128_bool_to_field(toBigEndian(u32_4_to_bool_128(r[4..8]))))
return r
"""
    main_block = []

    main_block.append("def main(field epoch_head, field[2] prev_block_hash, private field[{n_intermediate}][5] intermediate_blocks, field[5] final_block_field) -> (bool, field[5]):".format(n_intermediate=(n_blocks-1)))
    main_block.append("""
    u32 reference_target = unpack_field_to_4_u32(epoch_head)[2]
    u32[8] block_hash = [...unpack_field_to_4_u32(prev_block_hash[0]), ...unpack_field_to_4_u32(prev_block_hash[1])]
    u32 final_block_target = unpack_field_to_4_u32(final_block_field[4])[2]
    u32[{n_hashes}][8] blocks = [[0x00000000;8];{n_hashes}]
    for field i in 0..{n_intermediate} do
      block_hash = validate_block_header(reference_target, block_hash, intermediate_blocks[i])
      blocks[i] = block_hash
    endfor""".format(n_hashes=(n_blocks), n_intermediate=(n_blocks - 1)))

    main_block.append("""
    block_hash = validate_block_header(final_block_target, block_hash, final_block_field)
    blocks[{n_intermediate}] = block_hash
    bool targetValid, field target = validate_target(epoch_head, unpack_field_to_4_u32(intermediate_blocks[0][4])[1], final_block_target)
    field[2] merkle_root = compute_merkle_root(blocks)
    field[2] block = [u32_4_to_field(blocks[{n_intermediate}][0..4]), u32_4_to_field(blocks[{n_intermediate}][4..8])]
return targetValid, [target, ...block, ...merkle_root]
    """.format(n_intermediate=(n_blocks - 1)))
    return static_code + "\n".join(main_block)