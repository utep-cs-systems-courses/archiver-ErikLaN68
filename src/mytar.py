#! /usr/bin/env python3

import os
from sys import argv, exit

from buf import BufferedFdWriter, BufferedFdReader, bufferedCopy

# Will use \e as the end of line data line
def addFileTerm(byteAr):
    #checks for file term char
    temp = ''
    currentByte = ''
    for num,char in enumerate(byteAr):
        temp = temp + str(char)
        if len(temp) == 2:
            if temp == '\e':
                currentByte = currentByte + '\\'
                currentByte = currentByte + temp
            else:
                currentByte = currentByte + temp
        else:
            currentByte = currentByte + str(char)
    return currentByte + '\e'
                
        

if len(argv) < 2:
    print("Not a valid amount of inputs")
    exit

if argv[1] == 'c':
    
    inputFile = os.open(argv[2], os.O_RDONLY)
    fileContentsSize = os.path.getsize(inputFile)
    fileContents = os.read(inputFile, fileContentsSize)
    print("Size of file " + str(fileContentsSize))
    fileNameEncoded = argv[2].encode()
    encodeFileSize = fileContentsSize.to_bytes(10, 'big')
    print("The file size as a byte area " + str(encodeFileSize))
    print("The file size from bytes is " + str(int.from_bytes(encodeFileSize, "big")))
    fileNameSize = len(fileNameEncoded)
    print("The size of the file name " + str(fileNameSize))
    #newByteArray = fileNameSize.to_bytes(2, 'big') + fileNameEncoded + fileContentsSize.to_bytes(10, 'big') + fileContents
    newByteArray = fileNameSize.to_bytes(2, 'big') + fileNameEncoded + fileContents
    print(newByteArray)
    #Decodes the information and sends it to be put back to words
    bytearray
    exit

elif argv[1] == 'x':
    print('Will exract the files from a given mytar file')
    exit

else:
    print("Not a function of mytar")
    exit