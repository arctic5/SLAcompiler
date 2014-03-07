#!/usr/bin/python
 
import sys
 
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
    while code[currentCharToCheck] != '>': #Keep checking for replacements until we hit a close.
        if code[currentCharToCheck] == '.':
            print 'Now in second-level replacing: Classes.'
            newClass()
        elif code[currentCharToCheck] == "#":
            print 'Now in second-level replacing: IDs.'
            newId()
        else:
            newCode += code[currentCharToCheck]
            currentCharToCheck += 1 #If we didn't find anything to replace, write the code directly and move on.
    newCode += code[currentCharToCheck] #Append the >
    print 'Returning to lower level.'
 
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
print code
raw_input('Press Enter')
print 'GSLAUUA is now evaluating your code. Be patient!'
while len(code) != currentCharToCheck:
    print 'New loop'
    if code[currentCharToCheck] == '<':
        print 'Now in first level of replacing.'
        startReplacing()
    else:
        print 'Writing text.'
        newCode += code[currentCharToCheck] #There's probably a much better way to do this than write our code letter-for-letter.
    currentCharToCheck += 1
 
print 'Compilation complete.'
print newCode
compiledFileName = openThisFile,"compiled.sla"
blankFile = file(compiledFileName, 'w+')
raw_input('Press Enter')
#print "Good news! We have translated your SLA file to HTML!/nAll we need is a filename for your new code and we're done./nYou should probably end it in .html since that's what this is."
#newFilename = raw_input('>>')
#print 'GSLALUA is now saving', newFilename, 'in plain HTML.'
#with open(newFilename, 'w') as newFile:
#    newFile.write("{0}".format(str(newCode)))
 
#Test with <div#menu.slide></div>, see what comes out.