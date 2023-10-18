#! /usr/bin/env python3

import os
from sys import argv, exit, stdout

decode = True

from buf import BufferedFdWriter, BufferedFdReader, bufferedCopy

def getfileNameAndSize(fileName):
    fileNameEncoded = fileName.encode()
    fileNameSize = len(fileNameEncoded)
    encodeSize = fileNameSize.to_bytes(1, 'big')
    return encodeSize, fileNameEncoded

def getContentAndSize(fdInput):
    fileStatus = os.fstat(inputFile)
    contentSize = fileStatus.st_size
    fileContents = os.read(inputFile, contentSize)
    encodeFileSize = contentSize.to_bytes(2, 'big')
    return encodeFileSize, fileContents

def makeMyTarName(fileName):
    parts = fileName.split('.')
    return parts[0]
    
# Will use \e as the end of line data line
def frame(fdInput, fileName):
    fileNameSize,fileNameEncoded = getfileNameAndSize(fileName)
    fileContentsSize, fileContents = getContentAndSize(fdInput)
    
    if decode: print("Size of file " + str(fileContentsSize))
    if decode: print("The file size as a byte area " + str(int.from_bytes(fileContentsSize, "big")))
    if decode: print("The file size from bytes is " + str(fileContentsSize))
    if decode: print("The size of the file name " + str(fileNameSize))
    
    newByteArray = '-|'.encode() + fileNameSize + '-|'.encode() + fileNameEncoded + '-|'.encode() + fileContentsSize + '-|'.encode() + fileContents
    return newByteArray



if len(argv) < 2:
    print("Not a valid amount of inputs")
    exit

if argv[1] == 'c':
    argv.remove(argv[0])
    argv.remove(argv[0])
    myTarFileName = ''
    newByteArray = '-'.encode()
    for fileName in argv:
        inputFile = os.open(fileName, os.O_RDONLY)
        newByteArray = newByteArray + frame(inputFile, fileName)
        myTarFileName = myTarFileName + makeMyTarName(fileName)
    
    myTarFileName = myTarFileName + '.mytar'
    #Decodes the information and sends it to be put back to words
    outFile = os.open(myTarFileName, os.O_CREAT | os.O_WRONLY)
    os.write(outFile,newByteArray)
    exit

elif argv[1] == 'x':
    print('Will extract the files from a given mytar file')
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
    
    #print(filePart)
    if decode:
        print('File name size: ' + str(int.from_bytes(filePart[0], "big")))
        print('file name: ' + filePart[1].decode())
        print('content size is: ' + str(int.from_bytes(filePart[2], "big")))
        print('File name size: ' + str(int.from_bytes(filePart[4], "big")))
        print('file name: ' + filePart[5].decode())
        print('content size is: ' + str(int.from_bytes(filePart[6], "big")))
    
    print('src/outputtest/'+filePart[1].decode())
    # stdout = open('outputtest/'+filePart[1].decode(), "w" |c)
    # stdout.write(filePart[3])
    
    outFile = os.open('outputtest/'+filePart[1].decode(), os.O_CREAT | os.O_WRONLY)
    os.write(outFile,filePart[3])
    
    outFile = os.open('outputtest/'+filePart[5].decode(), os.O_CREAT | os.O_WRONLY)
    os.write(outFile,filePart[7])

else:
    print("Not a function of mytar")
    exit