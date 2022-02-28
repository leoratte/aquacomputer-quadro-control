#!/bin/python3

import sys

infile = open(sys.argv[1], 'rt')
outfile = open(sys.argv[2], 'wb')

for line in infile.readlines():
    for byte_str in line.split()[1:]:
        outfile.write(int(byte_str, 16).to_bytes(1, 'little'))
