import tkinter as tk
from tkinter import *
from tkinter import filedialog

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
        self.filemenu.add_command(label="New", command= lambda: spawn_new(master))
        self.filemenu.add_command(label="Open", command= lambda: open_file(self.text))
        self.filemenu.add_command(label="Save", command= lambda: save_file(self.text))

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Delete System32", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.config(menu=self.menubar)

        def save_file(textbox):
            filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            if filename != "":
                write_out(get_input(textbox), filename)

        def open_file(textbox):
            filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            write_in(filename, textbox)

        def write_in(filename, textbox):
            f = open(filename, 'r')
            contents = f.read()
            textbox.insert(INSERT, contents)

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


root = tk.Tk()
app = Veditor(root)
root.mainloop()
