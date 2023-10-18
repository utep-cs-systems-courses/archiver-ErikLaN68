#! /usr/bin/env python3

import os
from sys import argv, exit

decode = True

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
    if decode: print("Size of file " + str(fileContentsSize))
    fileNameEncoded = argv[2].encode()
    encodeFileSize = fileContentsSize.to_bytes(2, 'big')
    if decode: print("The file size as a byte area " + str(encodeFileSize))
    if decode: print("The file size from bytes is " + str(int.from_bytes(encodeFileSize, "big")))
    fileNameSize = len(fileNameEncoded)
    if decode: print("The size of the file name " + str(fileNameSize))
    newByteArray = '-|'.encode() + fileNameSize.to_bytes(1, 'big') + '-|'.encode() + fileNameEncoded + '-|'.encode() + fileContentsSize.to_bytes(2, 'big') + '-|'.encode() + fileContents
    #newByteArray = fileNameSize.to_bytes(2, 'big') + fileNameEncoded + fileContents
    if decode: print(newByteArray)
    #Decodes the information and sends it to be put back to words
    outFile = os.open('arch.mytar', os.O_CREAT | os.O_WRONLY)

    os.write(outFile,newByteArray)
    exit

elif argv[1] == 'x':
    print('Will exract the files from a given mytar file')
    inputFile = os.open(argv[2], os.O_RDONLY)
    fileContentsSize = os.path.getsize(inputFile)
    fileContents = os.read(inputFile, fileContentsSize)
    #print(fileContents)
    filePart = []
    tempByte = bytearray()
    preByte = 0
    read = False
    
    for i, byte in enumerate(fileContents):
        if i < (len(fileContents)-1):
            preByte = fileContents[i + 1]
            if byte == ord('-') and preByte == ord('|'):
                    if read:
                        filePart.append(tempByte)
                        tempByte = bytearray()
                    else:
                        read = True
        if read and byte != ord('-') and byte != ord('|'):
            tempByte.append(byte)
    filePart.append(tempByte)
    
    print(filePart)
    print('File name size is: ' + str(int.from_bytes(filePart[0], "big")))
    print('file name: ' + filePart[1].decode())
    print('content size is: ' + str(int.from_bytes(filePart[2], "big")))

else:
    print("Not a function of mytar")
    exit