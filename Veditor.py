import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os

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
        #"C:\Users\J.J. Varsity\AppData\Local\Programs\Python\Python36-32\python.exe"
        #"D:\Python3\python.exe"
        self.pythonpath = '"C:\\Users\\J.J. Varsity\\AppData\\Local\\Programs\\Python\\Python36-32\\python.exe"'

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
            input = textbox.get("1.0",'end-1c')
            return input
            
        def spawn_new(master):
            root = tk.Tk()
            new = Veditor(root)

        def kill(self):
            self.destroy()
        
        def run_script(filepath, pythonpath):
            filepath = '"'+filepath+'"'
            os.system('"'+pythonpath+' '+filepath+'"')

root = tk.Tk()
app = Veditor(root)
root.mainloop()
