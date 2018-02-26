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
        
        self.syntax = Syntax(self.text)
        if self.toggle:
            try:
                self.stop = self.master.after(500, lambda: self.syntax.dew_it(self.toggle))
            except Exception:
                pass
        # Useful Vars
        self.filepath = ''

        def set_python_path(path):
            self.pythonpath = os.path.abspath(path)
            #print(self.pythonpath)
            #self.pythonpath = '"'+path+'"'

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
            newRoot = Tk()
            newRoot.withdraw()
            if pathType:
                filename =filedialog.askopenfilename(initialdir="/", title="Select Python Path",
                                       filetypes=(("all files", "*.*"), ("text files", "*.txt")))
            else:
                filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                       filetypes=(("all files", "*.*"), ("text files", "*.txt")))
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
                f = open(filename, 'r')
                contents = f.read()
                textbox.insert(INSERT, contents)
                self.syntax.indent_open(textbox)
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

        def kill(self, stop):
            self.after_cancel(stop)
            self.destroy()

        def run_script(filepath, pythonpath):
            #filepath = '"' + filepath + '"'
            status = subprocess.Popen([self.pythonpath, self.filepath])
            #os.system('"' + pythonpath + ' ' + filepath + '"')

        def toggle_syntax(toggle, textbox):
            self.toggle = not toggle
            try:
                self.stop = self.master.after(500, lambda: self.syntax.dew_it(self.toggle))
            except Exception:
                pass
            
            #print(self.toggle)

class Syntax(tk.Text):
    def __init__(self, master):
        # tk.Text.__init__(self, master)
        self.master = master
        self.registeredKw = keyword.kwlist
        #print(self.registeredKw)
        self.registeredKw.extend(["False:", "True:", "else:", "try:", "return", "break"])
        #print(self.registeredKw
        self.indentLevel = [0]

        self.master.bind("<Return>", self.auto_indent)
        self.master.bind("<Tab>", self.tab)
        self.master.bind("<BackSpace>", self.back)

    def tab(self, arg):
        startLine = str(self.master.index("insert linestart"))
        endLine = str(self.master.index("insert lineend"))
        input = self.master.get(startLine, endLine).strip()
        if input == "":
           self.indentLevel[int(startLine[0])-1] +=1
        self.master.insert(INSERT, " " * 4)
        return "break"
    
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
        #print("actual pos "+actualPos)
        input = self.master.get(startLine, endLine).strip()
        colZero = re.search(r'([0-9]*\.0) |([0-9][0-9]*\.0)', actualPos)

        if self.master.tag_ranges("sel"):
            self.master.delete(SEL_FIRST,SEL_LAST)
        elif input == "" and not colZero and int(actualPos[pIndex:]) % 4 == 0:
            self.master.delete("insert -4 chars", "insert")
            if self.indentLevel[int(startLine[0])-1] > 1:
                self.indentLevel[int(startLine[0])-1] -= 1
            else:
                self.indentLevel[int(startLine[0])-1] = 0
        else:
            self.master.delete("insert -1 chars", "insert")
        return "break"
    
    def dew_it(self, toggle):
        #print("dew it"+str(toggle))
        if toggle:
            self.find_kw(self.master)
            self.find_quotes(self.master)
            self.find_comments(self.master)
            self.find_nums(self.master)
            #self.auto_indent(self.master)
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

    def find_quotes(self, textbox):
        lineNum = 1
        token = ""
        self.qCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            token = next.readline()
            # print(token)
            if token == "":
                break
            else:
                # wtf (?:"[^"]*\\(?:.[^"]*\\)*.[^"]*")|(?:"[^"]*") you may ask yourself.
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

    def find_comments(self, textbox):
        lineNum = 1
        token = ""
        self.comCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            token = next.readline()
            # print(token)
            if token == "":
                break
            else:
                inline = re.finditer(r'#.*', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in inline]

                for coord in tmp:
                    self.comCoords.append(coord)

                #block = re.finditer(r'', token)

                lineNum += 1

        self.color_coords(textbox, self.comCoords, "purple")

    def find_nums(self, textbox):
        lineNum = 1
        token = ""
        self.numCoords = []
        input = textbox.get("1.0", "end")
        next = io.StringIO(input)
        while True:
            token = next.readline()
            # print(token)
            if token == "":
                break
            else:
                inline = re.finditer(r'(([0-9][0-9]*\.[0-9][0-9]*)|([0-9][0-9]*))', token)
                tmp = [(str(lineNum) + "." + str(m.start()), str(lineNum) + "." + str(m.end())) for m in inline]

                for coord in tmp:
                    self.numCoords.append(coord)

                #block = re.finditer(r'', token)

                lineNum += 1

        self.color_coords(textbox, self.numCoords, "black")

    def auto_indent(self, arg):
        startLine = str(self.master.index("insert linestart"))
        endLine = str(self.master.index("insert lineend"))
        input = self.master.get(startLine, endLine)
        allInput = self.master.get("1.0", "end").splitlines()
        self.indentLevel = self.indentLevel[:len(allInput)]
        pIndex = 0
        for c in startLine:
            if c == ".":
                break
            else:
                pIndex += 1
        
        try:
            indentFill = self.indentLevel[int(startLine[:pIndex])-1]
        except IndexError:
            indentFill = 0
        if indentFill > 0:
            try:
                self.indentLevel[int(startLine[:pIndex])] = self.indentLevel[int(startLine[:pIndex])-1]
            except IndexError:
                if len(self.indentLevel) >= 1:
                    self.indentLevel.append(self.indentLevel[int(startLine[:pIndex])-1])
                else:
                    self.indentLevel.append(0)
             
        self.master.insert(INSERT, "\n")
        
        if re.search(r'.+\:', input):
            try:
                self.indentLevel[int(startLine[:pIndex])] = self.indentLevel[int(startLine[:pIndex])-1]+1
            except IndexError:
                self.indentLevel.append(self.indentLevel[int(startLine[:pIndex])-1] + 1)
            self.master.insert(INSERT, " " * (4 * self.indentLevel[int(startLine[:pIndex])]))
            #for i in range(int(startLine[:pIndex]),len(self.indentLevel)-1):
            #    try:
            #        self.indentLevel[i+1] = self.indentLevel[i]
            #    except IndexError:
            #        pass
            #print(self.indentLevel)
            return "break"

        try:
            self.master.insert(INSERT, " " * (4 * self.indentLevel[int(startLine[:pIndex])-1]))
            self.indentLevel[int(startLine[:pIndex])] = self.indentLevel[int(startLine[:pIndex])-1]
        except IndexError:
            self.indentLevel.append(self.indentLevel[int(startLine[:pIndex])-1])
            #self.indentLevel.append(0)
        return "break"

    def indent_open(self, textbox):
        input = textbox.get("1.0", "end").splitlines()
        #print(input[:13])
        for i in range(len(input)):
            spaceCount = 0
            for c in input[i]:
                if c == " ":
                    spaceCount += 1
                else:
                     try:
                         self.indentLevel[i] = int(spaceCount / 4)
                     except IndexError:
                         self.indentLevel.append(int(spaceCount / 4))
                     break
            self.indentLevel.append(0)
        #print(self.indentLevel)

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
# root.after(2000, lambda: syntax_highlight(app.text))
root.mainloop()
