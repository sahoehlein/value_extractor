

import pandas as pd 
import numpy as np
import re
import os
from tika import parser
from colorama import init, Fore
import glob
from tqdm import tqdm
import tkinter as tk

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
        self.regex_list = self.read_regex()
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
      
    def text_check(self, text, regex_list): 
        htext = text #copy of highlighted text 
        for regex in regex_list:
            htext = re.sub(regex, Fore.RED + r'\1' + Fore.RESET, htext) # overwrite terminal output 
        return htext
      
root = tk.Tk()
root.title("Regex Sanity Check App")
root.geometry('200x50')

app = articles_sanity_check(root)

app.mainloop()
