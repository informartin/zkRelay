#!/usr/bin/env python
import sys

def write_zokrates_file(code, path):
    with open(path, "w") as f:
        f.write(code)
