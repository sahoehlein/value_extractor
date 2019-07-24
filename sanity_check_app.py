import pandas as pd 
import numpy as np
import re
import os
from tika import parser
from colorama import init, Fore
import glob
from tqdm import tqdm
import tkinter as tk


class Ctxt(Text): # Custom Text Widget with Highlight Pattern   - - - - -
    # Credits to the owner of this custom class - - - - - - - - - - - - -
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)
        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
            
class articles_sanity_check(Frame):
    
    def __init__(self,master): 
        super(articles_sanity_check, self).__init__(master)
        self.grid()
        self.root = tk.Tk()
        self.idx = 0
        self.folderpath = '/Users/lukasmalik/Desktop/Masterarbeit/data/case_study/Stapel/unsuspicious'
        self.folder = glob.glob(self.folderpath + "/*.pdf")
        self.file = self.folder[idx]
        self.text = parser.from_file(self.file)['content']
        self.regex_list = read_regex()
        #self.htext = text_check(self.text, self.regex_list)
        self.create_widget()
    
    def create_widget(self): 
        # next button 
        self.nb = Button(self)
        self.nb['text'] = "Next article"
        self.nb['command'] = self.next_article
        self.nb.pack()
        
        # previous button 
        self.pb = Button(self)
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
        self.S.config(command=T.yview)

    def read_regex(regex_path = "regex_list.txt"):
        with open(regex_path) as f:
            regexes = f.readlines()
        return regexes    
    
    def next_article(self): 
        self.idx += 1
        self.file = self.folder[idx]
        self.text = parser.from_file(self.file)['content']
        self.htext = text_check(self.text, self.regex_list)
        self.T.insert(tk.END, self.htext)
        
    def previous_article(self): 
        self.idx -= 1
        self.file = self.folder[idx]
        self.text = parser.from_file(self.file)['content']
        self.htext = text_check(self.text, self.regex_list)
        self.T.insert(tk.END, self.htext)
      
#    def text_check(text, regex_list): 
#        htext = text #copy of highlighted text 
#        for regex in regex_list:
#            htext = re.sub(regex, Fore.RED + r'\1' + Fore.RESET, htext) # overwrite terminal output 
#        return htext
    
    def text_check(text, regex_list): 
        text = Ctxt(text)
        htext = text #copy of highlighted text 
        for regex in self.regex_list:
            htext.highlight_pattern(regex,'green', regexp=True)
        return htext

root = Tk()
root.title("Regex Sanity Check App")
root.geometry('200x50')

app = articles_sanity_check(root)

app.mainloop()