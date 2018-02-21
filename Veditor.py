import tkinter as tk
from tkinter import *
from tkinter import filedialog

def save_file(textbox):
    filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    write_out(get_input(textbox), filename)

def write_out(contents, fileName):
    f = open(fileName, 'w')
    f.write(contents)

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

filemenu.add_separator()

filemenu.add_command(label="Delete System32", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)
root.mainloop()
