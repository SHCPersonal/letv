#!/usr/bin/python
import sys

for line in sys.stdin:
        items=line.strip().split('\x01')
        if items[1] != '-':
            print items[1] + "\t" + "1"
        if items[2] != '-':
            print items[2] + "\t" + "1"
