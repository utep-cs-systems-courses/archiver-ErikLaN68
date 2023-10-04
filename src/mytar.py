#! /usr/bin/env python3

import os
from sys import argv, exit

if len(argv) < 2:
    print("Not a valid amount of inputs")
    exit

if argv[1] == 'c':
    print('Will create the tar file')
    fd = os.open(argv[2], os.O_RDONLY)
    print('File size ' + str(os.path.getsize(argv[2])))
    inputString = os.read(fd,os.path.getsize(argv[2]))
    print(inputString)
    exit

elif argv[1] == 'x':
    print('Will exract the files from a given mytar file')
    exit

else:
    print("Not a mytar function")
    exit

print("Hello World")