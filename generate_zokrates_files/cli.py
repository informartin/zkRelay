#!/usr/bin/env python
import sys

from generate_validation import generate_validation_code
from generate_root_computation import generate_root_code
from generate_merkle_proof_validation import generate_merkle_proof_validation_code

def write_zokrates_file(code, path):
    with open(path, "w") as f:
        f.write(code)


def main():
    arguments = len(sys.argv) - 1
    if arguments != 1:
        print('Irregular number of arguments. Arg. 1: Batch size')
        return
    batch_size = int(sys.argv[1])
    write_zokrates_file(generate_validation_code(batch_size), "validate.zok".format(i=batch_size))
    write_zokrates_file(generate_root_code(batch_size), "compute_merkle_root.zok".format(i=batch_size))
    write_zokrates_file(generate_merkle_proof_validation_code(batch_size), "verify_merkle_proof.zok".format(i=batch_size))
    

if __name__ == "__main__":
    main()
