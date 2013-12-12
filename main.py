from tkinter import *
from parse import parseFile, printTree2, searchTree

types = None
textbox = None
#sv = None


def printText(textstr):
    textbox.insert(END, textstr + "\n")


def callback(sv):
    textbox.delete(1.0, END)
    t = searchTree(types, sv.get())
    printTree2(t, printText)
    #print(t)
    #printTree2(types, printText)
    printText(sv.get())


if __name__ == "__main__":
    global textbox, types
    root = Tk()
    button = Button(root)
    button.grid(row=0, column=0)
    text = Text(root)
    #global sv
    sv = StringVar()
    textbox = text
    entry = Entry(root, textvariable=sv)
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    entry.grid(row=1, column=0)
    text.grid(row=2, column=0, columnspan=2)
    types = parseFile("test.cpp", printText)

    mainloop()