#!/usr/bin/python
import sys
import random

for line in sys.stdin:
    if len(line) > 8:
        r=random.randint(0, 2147483647)
        sys.stdout.write(str(r) + '\t' + line)
