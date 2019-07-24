import pandas as pd 
import numpy as np
import re
import os
from tika import parser
from colorama import init, Fore
import glob
from tqdm import tqdm
import tkinter as tk
 
#class Ctxt(Text): # Custom Text Widget with Highlight Pattern   - - - - -
#    # Credits to the owner of this custom class - - - - - - - - - - - - -
#    def __init__(self, *args, **kwargs):
#        Text.__init__(self, *args, **kwargs)
#
#    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
#                          regexp=False):
#        start = self.index(start)
#        end = self.index(end)
#        self.mark_set("matchStart", start)
#        self.mark_set("matchEnd", start)
#        self.mark_set("searchLimit", end)
#        count = tk.IntVar()
#        while True:
#            index = self.search(pattern, "matchEnd","searchLimit",
#                                count=count, regexp=regexp)
#            if index == "": break
#            self.mark_set("matchStart", index)
#            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
#            self.tag_add(tag, "matchStart", "matchEnd")
#            
class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=True):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        pattern = regex_list[0]
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
            
class articles_sanity_check(tk.Frame):
    
    def __init__(self,master): 
        super(articles_sanity_check, self).__init__(master)
        self.grid()
        self.root = tk.Tk()
        self.idx = 0
        self.folderpath = r'/Users/lukasmalik/Desktop/Masterarbeit/data/case_study/Stapel/unsuspicious'
        self.folder = glob.glob(self.folderpath + "/*.pdf")
        print(self.folder)
        self.file = self.folder[self.idx]
        print(self.file)
        self.text = parser.from_file(self.file)['content']
        print(self.text)
        self.regex_list = self.read_regex()
        print(self.regex_list)
        self.htext = self.text_check(self.text, self.regex_list)
        self.create_widget()
    
    def create_widget(self): 
        # next button 
        self.nb = tk.Button(self)
        self.nb['text'] = "Next article"
        self.nb['command'] = self.next_article
        self.nb.pack()
        
        # previous button 
        self.pb = tk.Button(self)
        self.pb['text'] = "Previous article"
        self.pb['command'] = self.previous_article
        self.pb.pack()

        self.T = tk.Text(self.root, height=50, width=50)
        self.T.pack(side=tk.LEFT, fill=tk.Y)
        self.T.insert(tk.END, self.htext)

        # scrollbar 
        self.S = tk.Scrollbar(self.root)
        self.S.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.T.config(yscrollcommand=self.S.set)
        self.S.config(command=self.T.yview)
        
    def read_regex(regex_path = str("regex_list.txt")):
        regex_path = "regex_list.txt"
        with open(regex_path) as f:
            regexes = f.readlines()
        return regexes    
    
    def next_article(self):
        self.idx += 1
        if self.idx == len(self.folder):
            self.idx = 0
        self.file = self.folder[self.idx]
        self.text = parser.from_file(self.file)['content']
        self.htext = self.text_check(self.text, self.regex_list)
        self.T.delete("1.0", tk.END)
        self.T.insert(tk.END, self.htext)
        
    def previous_article(self): 
        self.idx -= 1
        if self.idx == -1:
            self.idx = len(self.folder)-1
        
        self.file = self.folder[self.idx]
        self.text = parser.from_file(self.file)['content']
        self.htext = self.text_check(self.text, self.regex_list)
        self.T.delete("1.0", tk.END)
        self.T.insert(tk.END, self.htext)
      
#    def text_check(self, text, regex_list): 
#        htext = text #copy of highlighted text 
#        for regex in regex_list:
#            htext = re.sub(regex, Fore.RED + r'\1' + Fore.RESET, htext) # overwrite terminal output 
#        return htext
    def text_check(self, text, regex_list): 
        self.text = CustomText(self.text)
        self.htext = self.text #copy of highlighted text 
        for regex in regex_list:
            self.htext.highlight_pattern(regex,'green', regexp=True)
      
root = tk.Tk()
root.title("Regex Sanity Check App")
root.geometry('200x50')

app = articles_sanity_check(root)

app.mainloop()


#text = CustomText()
#text.tag_configure("red", foreground="#ff0000")
#    text.highlight_pattern("this should be red", "red")
