#!/usr/bin/env python3

import sys

def ignorePHP():
    global newCode
    global currentCharToCheck
    phpCodeUsed = 'true'
    while ((code[currentCharToCheck] != '?' or code[currentCharToCheck] != '%') and code[currentCharToCheck+1] != '>'): #This _should_ escape on both PHP and ASP, but if someone can test that please do.
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1
    
def ignoreComments():
    global newCode
    global currentCharToCheck
    while ((code[currentCharToCheck] + code[currentCharToCheck+1] + code[currentCharToCheck+2]) != '-->'):
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += "-->"
    currentCharToCheck += 2

def newUserAttribute():
    global newCode
    global currentCharToCheck
    endMarker = code[currentCharToCheck]
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1
    while code[currentCharToCheck] != endMarker:
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1

def newClass():
    global newCode
    global currentCharToCheck
    newCode += ' class="'
    currentCharToCheck += 1 # Replace . with ' class="'. NOTE THE SPACE. When replacing classes, .s will ALWAYS be transformed into a space. .s cannot be used for IDs or classes. It's not valid CSS.
    while code[currentCharToCheck] not in '#> ': # Keep checking until we hit a # (new id), a > (end of tag), or a space (undefined attribute)
        if code[currentCharToCheck] == '.': #Special code to group classes together
            newCode += ' '
        else:
            newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += '"' #And finish it off with the closing "! DO NOT ADD A SPACE since spaces are added before classes and ids already. Other spaces are user-defined.

def newId(): #Thankfully for me, ids are much easier to replace than classes.
    global newCode
    global currentCharToCheck
    newCode += ' id="'
    currentCharToCheck += 1
    while code[currentCharToCheck] not in '#> .':
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += '"'

def startReplacing():
    global newCode
    global currentCharToCheck
    newCode += code[currentCharToCheck] # Put in the <.
    currentCharToCheck += 1
    if code[currentCharToCheck] == '?' or code[currentCharToCheck] == '%': #Special code to ignore PHP and ASP blocks.
        ignorePHP()
    elif (code[currentCharToCheck] + code[currentCharToCheck+1] + code[currentCharToCheck+2]) == '!--':
        ignoreComments()
    else:
        while code[currentCharToCheck] != '>': # Keep checking for replacements until we hit a close.
            if code[currentCharToCheck] == '.': # .s are classes
                newClass()
            elif code[currentCharToCheck] == "#": # #s are ids
                newId()
            elif code[currentCharToCheck] in '"\'': # "s and 's are user attributes
                newUserAttribute()
            else:
                newCode += code[currentCharToCheck]
                currentCharToCheck += 1 #If we didn't find anything to replace, write the code directly and move on.
        newCode += code[currentCharToCheck] #Append the >

fileImported = 0
phpCodeUsed = 'false'
if len(sys.argv) != 1:
    oldFileName = sys.argv[1]
    if (oldFileName[-4:]) == '.sla':
        fileImported = 1
        openThisFile = oldFileName
if fileImported == 0:
    print('GSLAUUA - A simple hypertext markup language recompiler.')
    print('Please enter the name of your SLA formatted file below.')
    openThisFile = input('>>')
if len(openThisFile) == 0:
    print('Quit: No file opened.')
    sys.exit()
try:
    rawFileData = open(openThisFile, 'r') #r so we don't accidentally overwrite his code!
except IOError:
    print('Quit: Unable to open file.')
    sys.exit()
code = rawFileData.read()
rawFileData.close()
currentCharToCheck = 0
newCode = ''
print('GSLAUUA is now evaluating your code.')
while len(code) != currentCharToCheck:
    if code[currentCharToCheck] == '<':
        startReplacing()
    else:
        newCode += code[currentCharToCheck] #There's probably a much better way to do this than write our code letter-for-letter.
    currentCharToCheck += 1

#print(newCode)
#input('Press Enter')
if fileImported == 0:
    print("Your SLA-style file has been converted to HTML.")
    print("Please enter the name you want to save the file as, including extension.")
    newFilename = input('>>')
else:
    if phpCodeUsed == 'false':
        newFilename = oldFileName[:-4] + '.html'
    else:
        newFileName = oldFileName[:-4] + '.php'
print('GSLALUA is now saving ' + newFilename)
with open(newFilename, 'w') as newFile:
    newFile.write("{0}".format(str(newCode)))