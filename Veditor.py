import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import keyword
import re

root = tk.Tk()

class Veditor(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Veditor")
        #text area
        self.text = tk.Text(master, bg="darkgrey", fg="white")
        self.text.grid(sticky="nsew")
        #Menu Code
        self.menubar = tk.Menu(master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command= lambda: spawn_new(self.master))
        self.filemenu.add_command(label="Open", command= lambda: open_file(self.text))
        self.filemenu.add_command(label="Save", command= lambda: save_file(self.text))
        self.filemenu.add_command(label="Save as..", command= lambda: save_file_as(self.text))
        
        self.filemenu.add_separator()

        self.filemenu.add_command(label="Delete System32", command= lambda: kill(self.master))
        self.menubar.add_cascade(label="File", menu=self.filemenu)
	
        self.runmenu = tk.Menu(self.menubar, tearoff=0)
        self.runmenu.add_command(label="Run script", command= lambda: run_script(self.filepath, self.pythonpath))
        self.menubar.add_cascade(label="Run", menu=self.runmenu)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.config(menu=self.menubar)


        #Useful Vars
        self.filepath = ''
        #BEWARE HARDCODED PYTHONPATH

        self.pythonpath = '"C:\\Users\\J.J. Varsity\\AppData\\Local\\Programs\\Python\\Python36-32\\python.exe"' #Your python path

        def save_file(textbox):
            if len(self.filepath) > 0:
                write_out(get_input(textbox), self.filepath)
            else:
                save_file_as(textbox)
        
        def save_file_as(textbox):
            filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            if filename != "":
                write_out(get_input(textbox), filename)
                self.master.title("Veditor - "+filename)
                self.filepath = filename

        def open_file(textbox):
            filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            self.filepath=filename
            if filename != "":
                write_in(filename, textbox)
                self.master.title("Veditor - "+filename)

        def write_in(filename, textbox):
            # Remove text from textbox
            textbox.delete('1.0', END)
            try:
                f = open(filename, 'r')
                contents = f.read()
                textbox.insert(INSERT, contents)
            except FileNotFoundError:
                return

        def write_out(contents, fileName):
            try:
                f = open(fileName, 'w')
                f.write(contents)
            except FileNotFoundError:
                return

        def get_input(textbox):
            # get all text in textbox
            input = textbox.get("1.0", 'end-1c')
            return input
            
        def spawn_new(master):
            root = tk.Tk()
            new = Veditor(root)

        def kill(self):
            self.destroy()
        
        def run_script(filepath, pythonpath):
            filepath = '"'+filepath+'"'
            os.system('"'+pythonpath+' '+filepath+'"')


def syntax_highlight(textbox):
    charNum = 0
    lineNum = 1
    token = ""
    q = ""
    qCount = 0
    tmp = ["",""]
    registeredToks = keyword.kwlist
    kwCoords = []
    quoteCoords = []
    input = textbox.get("1.0", "end")
    for c in input:
        if c == ' ':
            if token in registeredToks:
                kwCoords.append((str(lineNum) + "." + str(charNum - len(token)), str(lineNum) + "." + str(charNum)))
            token = ""
            charNum += 1
        elif c == '\n':
            token = ""
            lineNum += 1
            charNum = 0
        elif c == '\"':
            q += c
            qCount += 1
            if qCount % 2 == 0:
                charNum += 1
                tmp[1] = str(lineNum) + "." + str(charNum)
                if q[0] and q[len(q)-1] == "\"":
                    quoteCoords.append(tmp)
                    tmp = ["",""]
                    #print(q)
                    q = ""
                    charNum += 1

            else:
                tmp[0] = str(lineNum) + "." + str(charNum)
            charNum += 1

        else:
            token += c
            charNum += 1

    for i in range(len(kwCoords)):
        textbox.tag_add("keyword", kwCoords[i][0], kwCoords[i][1])
    for i in range(len(quoteCoords)):
        try:
            textbox.tag_add("quotes", quoteCoords[i][0], quoteCoords[i][1])
        except TclError:
            print("woops")

    textbox.tag_config("keyword", foreground="blue")
    textbox.tag_config("quotes", foreground="green")
    #print(kwCoords)
    print(quoteCoords)
    root.after(2000, lambda: syntax_highlight(textbox))


app = Veditor(root)
root.after(2000, lambda: syntax_highlight(app.text))
root.mainloop()
