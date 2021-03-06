import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os.path
import sys
import subprocess
import keyword
import io
import re

root = tk.Tk()



class Veditor(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Veditor")
        self.stop = ""
        self.pythonpath = ""
        self.toggle = True
        # text area
        self.text = tk.Text(master, bg="darkgrey", fg="white")
        self.text.grid(sticky="nsew")
        
        # Menu Code
        self.menubar = tk.Menu(master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command= lambda : spawn_new(self.master))
        self.filemenu.add_command(label="Open", command= lambda : open_file(self.text))
        self.filemenu.add_command(label="Save", command= lambda : save_file(self.text))
        self.filemenu.add_command(label="Save as..", command= lambda : save_file_as(self.text))

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Delete System32", command= lambda : kill(self.master, self.stop))
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.runmenu = tk.Menu(self.menubar, tearoff=0)
        self.runmenu.add_command(label="Set python path", command=lambda: set_python_path(select_file(True)))
        self.runmenu.add_command(label="Run script", command= lambda : run_script(self.filepath, self.pythonpath))
        self.menubar.add_cascade(label="Run", menu=self.runmenu)

        self.stylemenu = tk.Menu(self.menubar, tearoff=0)
        self.stylemenu.add_command(label="Syntax Highlighting Toggle", command= lambda : toggle_syntax(self.toggle, self.text))
        self.menubar.add_cascade(label="Style", menu=self.stylemenu)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.config(menu=self.menubar)
        
        #initialize Syntax object
        self.syntax = Syntax(self.text)
        
        if self.toggle:
            try:
                #If syntax toggled on, apply syntax rules
                self.stop = self.master.after(500, lambda: self.syntax.dew_it(self.toggle))
            except Exception:
                pass
        # Useful Vars
        self.filepath = ''

        def set_python_path(path):
            self.pythonpath = os.path.abspath(path)

        def save_file(textbox):
            if len(self.filepath) > 0:
                write_out(get_input(textbox), self.filepath)
            else:
                save_file_as(textbox)

        def save_file_as(textbox):
            filename = filedialog.asksaveasfilename(initialdir="/", title="Save as..",
                                                    filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            if filename != "":
                write_out(get_input(textbox), filename)
                self.master.title("Veditor - " + filename)
                self.filepath = filename

        def select_file(pathType):
            # Spawn new root for file dialogue, suppress it visually
            newRoot = Tk()
            newRoot.withdraw()
            if pathType:
                filename =filedialog.askopenfilename(initialdir="/", title="Select Python Path",
                                       filetypes=(("all files", "*.*"), ("text files", "*.txt")))
            else:
                filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                       filetypes=(("all files", "*.*"), ("text files", "*.txt")))
            # Delete new root window to avoid memory leak, return file name
            newRoot.destroy()
            return filename
                

        def open_file(textbox):
            filename = select_file(False)
            
            self.filepath = os.path.abspath(filename)
            if filename != "":
                write_in(filename, textbox)
                self.master.title("Veditor - " + filename)

        def write_in(filename, textbox):
            # Remove text from textbox
            textbox.delete('1.0', END)
            try:
                # Write in text from file, handle exceptions
                f = open(filename, 'r')
                contents = f.read()
                textbox.insert(INSERT, contents)
            except FileNotFoundError:
                return
            

        def write_out(contents, fileName):
            try:
                # Write editor contents directly to file, handle exceptions
                f = open(fileName, 'w')
                f.write(contents)
            except FileNotFoundError:
                return

        def get_input(textbox):
            # get all text in textbox - last charcter
            input = textbox.get("1.0", 'end-1c')
            return input

        def spawn_new(master):
            # generate new veditor instance
            root = tk.Tk()
            new = Veditor(root)

        def kill(self, stop):
            # stop scheduled jobs, kill tkinter window/process
            self.after_cancel(stop)
            self.destroy()

        def run_script(filepath, pythonpath):
            # run current open file against user-set python path (if any)
            # Will fail if no python path is set 
            status = subprocess.Popen([self.pythonpath, self.filepath])

        def toggle_syntax(toggle, textbox):
            self.toggle = not toggle
            try:
                self.stop = self.master.after(500, lambda: self.syntax.dew_it(self.toggle))
            except Exception:
                pass
            


# The syntax class handles syntax highlighting and auto-indentation        
class Syntax(tk.Text):
    def __init__(self, master):
        self.master = master
        self.registeredKw = keyword.kwlist
        self.registeredKw.extend(["False:", "True:", "else:", "try:", "return", "break"])

        self.master.bind("<Return>", self.auto_indent)
        self.master.bind("<Tab>", self.tab)
        self.master.bind("<BackSpace>", self.back)

    # Tab macro. Inserts 4 spaces
    def tab(self, arg):
        self.master.insert(INSERT, " " * 4)
        return "break"
    
    # Backspace macro. removes 4 spaces if no text behind cursor
    # removes 1 space if at beginning of line or text behind cursor
    def back(self, arg):
        pIndex = 0
        startLine = str(self.master.index("insert linestart"))
        endLine = str(self.master.index("insert lineend"))
        actualPos = str(self.master.index("insert"))
        for c in actualPos:
            if c == ".":
                pIndex += 1
                break
            else:
                pIndex += 1

        input = self.master.get(startLine, actualPos).strip()
        
        # Check if we're at the beginning of the line
        colZero = re.search(r'([0-9]*\.0) |([0-9][0-9]*\.0)', actualPos)
        
        # Handle highlighted text deletion
        if self.master.tag_ranges("sel"):
            self.master.delete(SEL_FIRST,SEL_LAST)
        # elif there's no text behind the cursor, and we're at a position evenly divisible by four
        # delete 4 spaces
        elif input == "" and not colZero and int(actualPos[pIndex:]) % 4 == 0:
            self.master.delete("insert -4 chars", "insert")
        else:
        # Otherwise, delete 1 char
            self.master.delete("insert -1 chars", "insert")
        return "break"
        
    # This function runs the syntax highlighting
    def dew_it(self, toggle):
        # If syntax highlighting is on
        # run color methods
        if toggle:
            self.find_kw(self.master)
            self.find_quotes(self.master)
            self.find_comments(self.master)
            self.find_nums(self.master)
            try:
                self.stop = self.master.after(500, lambda: self.dew_it(toggle))
            except Exception:
                pass
            self.master.tag_remove("white", "1.0","end")
        else:
            try:
                self.master.after_cancel(self.stop)
            except Exception:
                pass
            self.master.tag_add("white", "1.0", "end")
            self.master.tag_config("white", foreground="white")
        return
        
    # This function finds keywords for syntax highlighting.
    # NOTE: Re-do this with regex
    def find_kw(self, textbox):
        charNum = 0
        lineNum = 1
        token = ""
        self.kwCoords = []
        input = textbox.get("1.0", "end")
        for c in input:
            if c == ' ' or c == '\t':
                if token in self.registeredKw:
                    self.kwCoords.append(
                        (str(lineNum) + "." + str(charNum - len(token)), str(lineNum) + "." + str(charNum)))
                token = ""
                charNum += 1
            elif c == '\n':
                if token in self.registeredKw:
                    self.kwCoords.append(
                        (str(lineNum) + "." + str(charNum - len(token)), str(lineNum) + "." + str(charNum)))
                token = ""
                lineNum += 1
                charNum = 0
            else:
                token += c
                charNum += 1
        self.color_coords(textbox, self.kwCoords, "blue")
    
    #This function finds quotes for syntax highlighting
    def find_quotes(self, textbox):
        lineNum = 1
        token = ""
        self.qCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            token = next.readline()
            if token == "":
                break
            else:
                # wtf is even (?:"[^"]*\\(?:.[^"]*\\)*.[^"]*")|(?:"[^"]*") you may ask yourself.
                # wtf =  ((qn*b(an*b)*an*q) | (qn*q))
                # where q = quote " , n = any non-quote [^"], b = backslash \, a = any character .
                # Credit: https://mail.python.org/pipermail/tutor/2003-December/027063.html

                iter = re.finditer(r'(?:"[^"]*\\(?:.[^"]*\\)*.[^"]*")|(?:"[^"]*")', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in iter]

                for coord in tmp:
                    self.qCoords.append(coord)

                iter = re.finditer(r'(?:\'[^\']*\\(?:.[^\']*\\)*.[^\']*\')|(?:\'[^\']*\')', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in iter]

                for coord in tmp:
                    self.qCoords.append(coord)

                lineNum += 1

        self.color_coords(textbox, self.qCoords, "green")
    
    # This function finds line comments for highlighting
    def find_comments(self, textbox):
        lineNum = 1
        token = ""
        self.comCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            # Read input line by line
            token = next.readline()
            if token == "":
                break
            else:
                inline = re.finditer(r'#.*', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in inline]

                for coord in tmp:
                    self.comCoords.append(coord)

                lineNum += 1

        self.color_coords(textbox, self.comCoords, "purple")
    
    # This  function finds numbers for highlighting
    def find_nums(self, textbox):
        lineNum = 1
        token = ""
        self.numCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            token = next.readline()
            if token == "":
                break
            else:
                inline = re.finditer(r'(([0-9][0-9]*\.[0-9][0-9]*)|([0-9][0-9]*))', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in inline]

                for coord in tmp:
                    self.numCoords.append(coord)

                lineNum += 1

        self.color_coords(textbox, self.numCoords, "black")
    
    # This function implements auto-indentation
    def auto_indent(self, arg):
        # Get current line of text
        startLine = str(self.master.index("insert linestart"))
        endLine = str(self.master.index("insert lineend"))
        input = self.master.get(startLine, endLine)
        
        # Compute current indentdation level
        curLevel = self.current_level(input)
        # Check character behind cursor
        bCursor = self.getCharBehindCursor()     
        self.master.insert(INSERT, "\n")
        
        if bCursor == ":":
            # If the character behind the cursor is ":"
            # Indent by previous indent + 1
            self.master.insert(INSERT, " " * (4* (curLevel + 1)))
            return "break"
        else:
            # Otherwise, indent by current indent level
            self.master.insert(INSERT, " " * (4* curLevel))
            return "break"
    
    # This function gets the character directly behind the cursor
    def getCharBehindCursor(self):
        char = self.master.get("%s-1c" % INSERT, INSERT)
        return char
                    
    # This function computes the current indentation level
    def current_level(self, input):
        spaceCount = 0
        for c in input:
            if c == " ":
                spaceCount += 1
            else:
                return int(spaceCount / 4)
        return int(spaceCount / 4)

    # This function applies the colors to the tagged text
    # According to syntax
    def color_coords(self, textbox, coords, color):
        if color == "blue":
            for i in range(len(coords)):
                textbox.tag_add("keyword", self.kwCoords[i][0], self.kwCoords[i][1])
            textbox.tag_config("keyword", foreground="blue")
        if color == "green":
            for i in range(len(coords)):
                textbox.tag_add("quote", self.qCoords[i][0], self.qCoords[i][1])
            textbox.tag_config("quote", foreground="green")
        if color == "purple":
            for i in range(len(coords)):
                textbox.tag_add("comment", self.comCoords[i][0], self.comCoords[i][1])
            textbox.tag_config("comment", foreground="purple")
        if color == "black":
            for i in range(len(coords)):
                textbox.tag_add("number", self.numCoords[i][0], self.numCoords[i][1])
            textbox.tag_config("number", foreground="black")



app = Veditor(root)
root.mainloop()
