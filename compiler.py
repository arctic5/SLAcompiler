#!/usr/bin/env python3

import sys
import traceback

def ignorePHP():
    global newCode
    global position
    phpCodeUsed = 'true'
    while ((code[position] != '?' or code[position] != '%') and code[position+1] != '>'):
        newCode += code[position]
        position += 1
    newCode += code[position]
    position += 1

def ignoreScripts():
    global newCode
    global position
    while (code[position] + code[position+1] + code[position+2] + code[position+3] + code[position+4] + code[position+5] + code[position+6] + code[position+7] + code[position+8] != '</script>'): #Turns out even if it's in a string, HTML just says "fvck everything" when it comes to </script>.
        newCode += code[position]
        position += 1
    #"/script>" won't be checked by the parser so we can just let the code write itself.

def ignoreComments():
    global newCode
    global position
    while ((code[position] + code[position+1] + code[position+2]) != '-->'):
        newCode += code[position]
        position += 1
    newCode += "-->"
    position += 2

def newUserAttribute():
    global newCode
    global position
    endMarker = code[position]
    newCode += code[position]
    position += 1
    while code[position] != endMarker:
        newCode += code[position]
        position += 1
    newCode += code[position]
    position += 1

def newClass():
    global newCode
    global position
    newCode += ' class="'
    position += 1 # Replace . with ' class="'. NOTE THE SPACE. When replacing classes, .s will ALWAYS be transformed into a space. .s cannot be used for IDs or classes. It's not valid CSS.
    while code[position] not in '#> ': # Keep checking until we hit a # (new id), a > (end of tag), or a space (undefined attribute)
        if code[position] == '.': #Special code to group classes together
            newCode += ' '
        else:
            newCode += code[position]
        position += 1
    newCode += '"' #And finish it off with the closing "! DO NOT ADD A SPACE since spaces are added before classes and ids already. Other spaces are user-defined.

def newId(): #Thankfully for me, ids are much easier to replace than classes.
    global newCode
    global position
    newCode += ' id="'
    position += 1
    while code[position] not in '#> .':
        newCode += code[position]
        position += 1
    newCode += '"'

def startReplacing():
    global newCode
    global position
    scriptUsed = 'false'
    newCode += code[position] # Put in the <.
    position += 1
    #Special escapes
    if code[position] == '?' or code[position] == '%':
        ignorePHP()
    elif (code[position] + code[position+1] + code[position+2]) == '!--':
        ignoreComments()
    else:
        if (code[position] + code[position+1] + code[position+2] + code[position+3] + code[position+4] + code[position+5]) == 'script':
            scriptUsed = 'true' #we're delaying this so we can still check for classes and IDs on the <script> tag. I don't know why you'd want to do that but hell someone probably has a reason.
        while code[position] != '>': # Keep checking for replacements until we hit a close.
            if code[position] == '.': # .s are classes
                newClass()
            elif code[position] == "#": # #s are ids
                newId()
            elif code[position] in '"\'': # "s and 's are user attributes
                newUserAttribute()
            else:
                newCode += code[position]
                position += 1 #If we didn't find anything to replace, write the code directly and move on.
        if scriptUsed == 'true': #ignore script blocks
            ignoreScripts()
        newCode += code[position] #Append the >

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
position = 0
newCode = ''
print('GSLAUUA is now evaluating your code.')
try:
    while len(code) != position:
        if code[position] == '<':
            startReplacing()
        else:
            newCode += code[position] #There's probably a much better way to do this than write our code letter-for-letter.
        position += 1
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
