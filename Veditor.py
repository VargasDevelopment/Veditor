import tkinter as tk
from tkinter import *

def save_file(textbox):
    newWindow = tk.Toplevel(root)
    label = tk.Label(newWindow,text="file name/extension")
    label.pack(side=LEFT)
    textEntry = tk.Entry(newWindow, bd=10)
    textEntry.pack(side=RIGHT)
    button = tk.Button(newWindow, text="Submit", command=lambda : write_out(get_input(textbox), textEntry.get(), newWindow))
    button.pack()


def write_out(contents, fileName, win):
    f = open(fileName, 'w')
    f.write(contents)
    win.destroy()

def get_input(textbox):
    input = textbox.get("1.0",'end-1c')
    return input

def donothing():
   
   filewin = tk.Toplevel(root)
   button = tk.Button(filewin, text="Do nothing button")
   button.pack()

root=tk.Tk("text editor")
root.title("Veditor")

#stuff goes here
text = tk.Text(root, bg="darkgrey", fg="white")
text.grid()

#Menu code
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command= lambda: save_file(text))
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Delete System32", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)




root.config(menu=menubar)
root.mainloop()
