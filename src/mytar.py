#! /usr/bin/env python3

import os
from sys import argv, exit, stdout

debug = False
debugGif = False

from buf import BufferedFdWriter, BufferedFdReader, bufferedCopy

def getfileNameAndSize(fileName):
    fileNameEncoded = fileName.encode()
    return fileNameEncoded

def getContentAndSize(fdInput):
    fileStatus = os.fstat(fdInput)
    contentSize = fileStatus.st_size
    fileContents = os.read(fdInput, contentSize)
    ###Test###
    if debugGif:
        outFile = os.open('outputtest/test.gif', os.O_CREAT | os.O_WRONLY)
        print('file contents is of type ' + str(type(fileContents)))
        byteArrayCont = bytearray(fileContents)
        print('file contents is of type ' + str(type(byteArrayCont)))
        os.write(outFile,byteArrayCont)
    #########
    return fileContents

def makeMyTarName(fileName):
    parts = fileName.split('.')
    return parts[0]

# Will use -| as the end of line data line
def frame(fdInput, fileName):
    fileNameEncoded = getfileNameAndSize(fileName)
    fileContents = getContentAndSize(fdInput)
    
    if debug: 
        print("The size of the file name " + str(fileNameEncoded))
    
    newByte = fileNameEncoded + '-|'.encode() + fileContents + '-|'.encode()
    if debug: print(newByte)
    
    return newByte

def createMyTar(myTarFileName,newByte):
    #outFile = os.open(1, os.O_CREAT | os.O_WRONLY)
    os.write(1,newByte)
    os.close(1)

def framer(argv):
    myTarFileName = ''
    newByte = ''.encode()
    for fileName in argv:
        inputFile = os.open(fileName, os.O_RDONLY)
        newByte = newByte + frame(inputFile, fileName)
        myTarFileName = myTarFileName + makeMyTarName(fileName)
    
    myTarFileName = myTarFileName + '.mytar'
    
    createMyTar(myTarFileName,newByte)

def puller(fileContents):
    filePart = []
    tempByte = bytearray()
    skip = False
    for i, byte in enumerate(fileContents):
        if i < len(fileContents)-1:
            nextByte = fileContents[i + 1]
            if byte == ord('-') and nextByte == ord('|'):
                filePart.append(tempByte)
                tempByte = bytearray()
                skip = True
            if skip == False:
                tempByte.append(byte)
            if skip and byte == ord('|'):
                skip = False
    return filePart

def createFromMyTar(filePart):
    for index, tarPart in enumerate(filePart):
        if index == 0 or index % 2 == 0:
            outFile = os.open('outputtest/'+tarPart.decode(), os.O_CREAT | os.O_WRONLY)
        else:
            os.write(outFile,bytes(tarPart))
            os.close(outFile)

def deFramer(inputFileName):
    fdInput = os.open(inputFileName, os.O_RDONLY)
    fileStatus = os.fstat(fdInput)
    size = fileStatus.st_size
    fileContents = os.read(fdInput, size)
    
    filePart = puller(fileContents)
                
    if debug:
        print(filePart)
        print('file name: ' + filePart[0].decode())
    
    createFromMyTar(filePart)


if len(argv) < 2:
    #print("Not a valid amount of inputs")
    exit

if argv[1] == 'c':
    argv.remove(argv[0])
    argv.remove(argv[0])
    #print("Creating a new .mytar file from given files")
    framer(argv)
    exit

elif argv[1] == 'x':
    #print('Extracting the files from the given .mytar file')
    deFramer(argv[2])
    
    # # print('src/outputtest/'+filePart[1].decode())
    # # stdout = open('outputtest/'+filePart[1].decode(), "w" |c)
    # # stdout.write(filePart[3])
    # os.write(just use stdout here and the OS will handle the rest or 1)
    # # outFile = os.open('outputtest/'+filePart[5].decode(), os.O_CREAT | os.O_WRONLY)
    # # os.write(outFile,filePart[7])

else:
    print("Not a function of mytar")
    exit