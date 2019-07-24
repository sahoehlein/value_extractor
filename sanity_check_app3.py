

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
        #self.folder = ["3A.pdf", "5A.pdf"]

        print(self.folder)
        self.file = self.folder[self.idx]
        print(self.file)
        self.text = parser.from_file(self.file)['content']
        self.regex_list = self.read_regex()
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
        self.T.insert('1.0', self.text)

        # scrollbar
        self.S = tk.Scrollbar(self.root)
        self.S.pack(side=tk.RIGHT, fill=tk.Y)

        self.T.config(yscrollcommand=self.S.set)
        self.S.config(command=self.T.yview)

        self.highlight_text(self.text, self.regex_list)

    def read_regex(self, regex_path = "regex_list.txt"):
        f = open(regex_path, 'r')
        regexes = [eval(item) for item in f.read().splitlines()]
        f.close()

        return regexes

    def next_article(self):
        self.idx += 1
        if self.idx == len(self.folder):
            self.idx = 0
        self.file = self.folder[self.idx]
        self.text = parser.from_file(self.file)['content']

        self.T.delete("1.0", tk.END)
        self.T.insert(tk.END, self.text)

        # Note: we first need to insert the text, then we can highlight it
        self.highlight_text(self.text, self.regex_list)

    def previous_article(self):
        self.idx -= 1
        if self.idx == -1:
            self.idx = len(self.folder)-1

        self.file = self.folder[self.idx]
        self.text = parser.from_file(self.file)['content']

        self.T.delete("1.0", tk.END)
        self.T.insert(tk.END, self.text)

        self.highlight_text(self.text, self.regex_list)

    def highlight_text(self, text, regex_list):
        ''' This function will highlight text based on regex_list '''

        for regex in regex_list:

            # We first need to get all lines from our Text widget (as a list)
            lineList = self.T.get('1.0', 'end-1c').splitlines()
            # Now we iterate over them and check if line contain our regex expression
            for i in range( len(lineList) ):
                currentLine = lineList[i]

                # we can simply find start and end index from our regex match and highlight it from there
                obj = re.finditer(regex, currentLine)
                for item in obj:
                    start = item.start(0)
                    end = item.end(0)

                    # In order for us to color the text from start and end index, we need first to mark it with a tag
                    self.T.tag_add("color_me", "{}.{}".format(i+1, start), "{}.{}".format(i+1, end))

                    #print("{}:{}".format(start, end))



        # Then simply set background of all marked tag to desierd color
        self.T.tag_config("color_me", background="yellow")

root = tk.Tk()
root.title("Regex Sanity Check App")
root.geometry('200x50')

app = articles_sanity_check(root)

app.mainloop()
