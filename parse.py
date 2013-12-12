import re


def insertSpaces(line, token):
    tline = str(line)
    for t in token:
        tline = tline.replace(t, ' ' + t + ' ')
    return tline


def parseFile(filename, printFunction):
    data = ""
    lineNumber = 0

    for line in open(filename):
        lineNumber += 1
        if len(line):
            if line[0] == '#':
                pass
            else:
                data += line + " <" + str(lineNumber) + "> "
                #print(line.rstrip())
    del line

    data = re.sub('".*"', '""', data)
    data = data.replace('\n', ' ')
    data = insertSpaces(data, ';{}(),')
    data = data.replace('\t', ' ')
    data = re.sub('[ ]+', ' ', data)

    splitted = data.split()
    types = {}
    parseTokens(tokens=splitted, types=types, stack=[types])
    print("Resultatet")
    printTree2(types, printFunction)
    return types


def pushstack(s, o):
    s.append(o)


def popstack(s):
    s.pop()
    return s[-1]


def topstack(s, o):
    if not s[-1] is o:
        s.append(o)


class MetaInfo:
    fileLine = 0
    type = ""

    def __init__(self, type, line):
        self.type = type
        self.fileLine = line

    def toString(self):
        return self.type + " rad " + self.fileLine


def parseTokens(tokens, types, stack, recursed=0, paradepth=0, currentLine=0):
    token = tokens.pop(0)
    current = types
    while token:
        if token == "class":
            token = tokens.pop(0)
            t = stack[-1][token] = {"meta": MetaInfo("class", currentLine)}
            current = t
        elif token == "int":
            token = tokens.pop(0)
            t = stack[-1][token] = {"meta": MetaInfo("int", currentLine)}
            if paradepth is 0:  #annars är det troligen argument till en funktion
                current = t
        elif token is ";":
            current = stack[-1]
        elif token is "(":
            topstack(stack, current)
            paradepth += 1
        elif token is ")":
            paradepth -= 1
        elif token[0] == '<' and token[-1] == '>':
            currentLine = str(token[1:-1])
        if token is "}":
            popstack(stack)
            return

        print("\t" * recursed + token)

        if token is "{":
            topstack(stack, current)
            parseTokens(tokens, types, stack, recursed + 1, paradepth, currentLine)
            current = stack[-1]

        if tokens:
            token = tokens.pop(0)
        else:
            token = ""


def printObject(object, recursion=0):
    print("\t" * recursion, end="")
    if object.__class__ is str:
        print("\t" * recursion + object)
    if object.__class__ is dict:
        for o in object:
            member = object[o]
            if member.__class__ is str:
                printObject(member + " " + o)
            elif member.__class__ is dict:
                printObject(o)
                printObject(object[o], recursion + 1)


def printTree(tree, printfunk=print, depth=0):
    if tree.__class__ is MetaInfo:
        pass
    elif not tree:
        printfunk("\t" * depth + "-")
    elif tree.__class__ is str:
        printfunk("\t" * depth + tree)
    else:
        for key, val in tree.items():
            printfunk("\t" * depth + key)
            printTree(val, printfunk, depth + 1)


def printTree2(tree, printfunk=print, stack=[]):
    if tree.__class__ is MetaInfo:
        printfunk(".".join(str(x) for x in stack) + " " + tree.toString())
        pass
    elif not tree:
        printfunk(".".join(str(x) for x in stack) + "-")
    elif tree.__class__ is str:
        #printfunk(".".join(str(x) for x in stack) + " = " + tree)
        pass
    elif tree.__class__ is dict:
        newStack = stack[:]
        for key, val in tree.items():
            newStack.append(key)
            beginning = ""
            if val.__class__ is str:
                beginning = str(val + " ")
            printfunk(beginning + ".".join(str(x) for x in newStack))
            printTree2(val, printfunk, newStack)
            newStack.pop()


def searchTree(types, line):
    found = dict()
    if len(line) < 2:
        return types
    if not types.__class__ is dict:
        return
    for key, val in types.items():
        if key.find(line) > -1:
            found[key] = dict()
        if types.__class__ is dict:
            res = searchTree(val, line)
            if res.__class__ is dict:
                for k, v in res.items():
                    if not key in found:
                        found[key] = dict()
                    found[key][k] = v
            elif res.__class__ is str:
                pass
    return found


if __name__ == "__main__":
    parseFile("test.cpp")