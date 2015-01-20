#!/usr/bin/env python3

import sys
import traceback

def ignorePHP():
    global newCode
    global currentCharToCheck
    phpCodeUsed = 'true'
    while ((code[currentCharToCheck] != '?' or code[currentCharToCheck] != '%') and code[currentCharToCheck+1] != '>'):
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1

def ignoreScripts():
    global newCode
    global currentCharToCheck
    while (code[currentCharToCheck] + code[currentCharToCheck+1] + code[currentCharToCheck+2] + code[currentCharToCheck+3] + code[currentCharToCheck+4] + code[currentCharToCheck+5] + code[currentCharToCheck+6] + code[currentCharToCheck+7] + code[currentCharToCheck+8] != '</script>'): #Turns out even if it's in a string, HTML just says "fvck everything" when it comes to </script>.
        newCode += code[currentCharToCheck]
        currentCharToCheck += 1
    #"/script>" won't be checked by the parser so we can just let the code write itself.

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
    scriptUsed = 'false'
    newCode += code[currentCharToCheck] # Put in the <.
    currentCharToCheck += 1
    #Special escapes
    if code[currentCharToCheck] == '?' or code[currentCharToCheck] == '%':
        ignorePHP()
    elif (code[currentCharToCheck] + code[currentCharToCheck+1] + code[currentCharToCheck+2]) == '!--':
        ignoreComments()
    else:
        if (code[currentCharToCheck] + code[currentCharToCheck+1] + code[currentCharToCheck+2] + code[currentCharToCheck+3] + code[currentCharToCheck+4] + code[currentCharToCheck+5]) == 'script':
            scriptUsed = 'true' #we're delaying this so we can still check for classes and IDs on the <script> tag. I don't know why you'd want to do that but hell someone probably has a reason.
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
        if scriptUsed == 'true': #ignore script blocks
            ignoreScripts()
        newCode += code[currentCharToCheck] #Append the >

fileImported = 'false'
phpCodeUsed = 'false'
if len(sys.argv) != 1:
    oldFileName = sys.argv[1]
    if (oldFileName[-4:]) == '.sla':
        fileImported = 'true'
        openThisFile = oldFileName
if fileImported == 'false':
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
try:
    while len(code) != currentCharToCheck:
        if code[currentCharToCheck] == '<':
            startReplacing()
        else:
            newCode += code[currentCharToCheck] #There's probably a much better way to do this than write our code letter-for-letter.
        currentCharToCheck += 1
except (RuntimeError, TypeError, NameError, IndexError) as e:
    print('\n\
        ========================================\n\
        Woah! GSLAUUA just encountered an error!\n\
        ========================================\n\
The error Python gave us was "' + e.__class__.__name__ + '".\n\
We recommend combing through your code and making sure that nothing is wrong\n\
syntatically. Some things to watch out for:\n\
 - You left a left carat (<) open. (I.E., with no right carat [>].)\n\
 - You opened an attribute using a quote or apostrophe, but forgot to close it.\n\
 - You opened an attribute with one opener, but closed it with a different one.\n\
 - You opened up PHP or ASP, but didn\'t close it appropriately.\n\n\
If all of these things have been checked and you\'re still getting an error, let\n\
us know over at http://github.com/arctic5/SLAcompiler/issues\n\
When you press enter, we\'ll give you some details about the error. Include\n\
these details if you plan to post an issue to GitHub!')
    input('Press enter to continue...')
    print("\n" + traceback.format_exc())
    input('Press enter to continue...')
    sys.exit()

#print(newCode)
#input('Press Enter')
if fileImported == 'false':
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
