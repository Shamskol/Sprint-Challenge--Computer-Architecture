#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) < 2:
    print("Must specify a program to run")

program = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        code = line.split("#")[0]
        if code.strip():
            program.append(int(code.strip(), 2))

# print(program)
cpu = CPU()

cpu.load(program)
cpu.run()
