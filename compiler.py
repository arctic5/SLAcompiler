#!/usr/bin/env python2.7
 
import sys
 
def newUserAttribute():
    global newCode
    global currentCharToCheck
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1
    while code[currentCharToCheck] != '"':
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
    print code[currentCharToCheck]
    newCode += code[currentCharToCheck]
    currentCharToCheck += 1
    print code[currentCharToCheck]
    while code[currentCharToCheck] != '>': #Keep checking for replacements until we hit a close.
        if code[currentCharToCheck] == '.':
            newClass()
        elif code[currentCharToCheck] == "#":
            newId()
        elif code[currentCharToCheck] == '"':
            newUserAttribute()
        else:
            newCode += code[currentCharToCheck]
            currentCharToCheck += 1 #If we didn't find anything to replace, write the code directly and move on.
    newCode += code[currentCharToCheck] #Append the >
def writeCompiledToFile(name,string):
    nameAndExtension = (name+"compiled.html")
    compiled = open(nameAndExtension, 'w')
    compiled.write(string)
 
print 'GSLAUUA v0.01 alpha - A simple hypertext markup language recompiler.'
print 'Because GSLAUUA is more pronouncable than SHTMLR!'
print 'Please enter the name of your SLA formatted file below.'
openThisFile = raw_input('>>')
if len(openThisFile) == 0:
    print 'Quit: No file opened.'
    sys.exit()
try:
    rawFileData = open(openThisFile, 'r') #r so we don't accidentally overwrite his code!
except IOError:
    print 'Quit: Unable to open file.'
    sys.exit()
code = rawFileData.read()
rawFileData.close()
currentCharToCheck = 0
newCode = ''
print 'GSLAUUA is now evaluating your code. Be patient!'
while len(code) != currentCharToCheck:
    if code[currentCharToCheck] == '<':
        startReplacing()
    else:
        newCode += code[currentCharToCheck] #There's probably a much better way to do this than write our code letter-for-letter.
    currentCharToCheck += 1
 
print 'Compilation complete.'
print newCode
writeCompiledToFile(openThisFile,newCode)
raw_input('Press Enter')
#print "Good news! We have translated your SLA file to HTML!/nAll we need is a filename for your new code and we're done./nYou should probably end it in .html since that's what this is."
#newFilename = raw_input('>>')
#print 'GSLALUA is now saving', newFilename, 'in plain HTML.'
#with open(newFilename, 'w') as newFile:
#    newFile.write("{0}".format(str(newCode)))
 
#Test with <div#menu.slide></div>, see what comes out.