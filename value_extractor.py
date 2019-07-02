'''
This file reads pdfs from a folder and extracts statistical values and writes them to csv 
It contains a function to print a highlighted version of the text for a sanity check
It contains a function to perform sanity check on regular expressions 
'''

import pandas as pd 
import numpy as np
import re
import os
from tika import parser
from colorama import init, Fore
import glob
from tqdm import tqdm


#def read_regex(regex_path = "regex_list.txt"):
#    '''
#    input: string, path to regex list saved as txt 
#    output: list, regex expression, one per line  
#    '''
#    with open(regex_path) as f:
#        regexes = f.read().splitlines() 
#    return regexes 

def dict_from_text(text, regex_list): 
    '''
    input text and list of regex expressions 
    output highlighted text and dictionary of regex and values 
    '''
    vdict = {'regex':[], 'value':[]} # value dict 
    for regex in regex_list:
        values = re.findall(regex,text)
        for value in values:
            vdict['regex'].append(regex)
            vdict['value'].append(value)
    vdict = pd.DataFrame(vdict)
    return vdict

def get_values(folderpath):
    '''
    input folderpath with pdf files 
    output csv with file, regex and values 
    '''
    folder = glob.glob(folderpath + "/*.pdf")
    
    df = pd.DataFrame()
   
    for file in tqdm(folder): 
        text = parser.from_file(file)['content']
        # get vdict
        vdict = dict_from_text(text, regex_list)
        df.append([file.split(os.path.sep)[-1]] * len(vdict['value']))
        df.append(vdict['regex'])
        found.append(vdict['value'])

    df.to_csv('extracted.csv', sep = ';')
    return df 
    
def get_values(folderpath):
    '''
    input folderpath with pdf files 
    output csv with file, regex and values 
    '''
    folder = glob.glob(folderpath + "/*.pdf")
    
    df = pd.DataFrame()
   
    for file in tqdm(folder): 
        text = parser.from_file(file)['content']
        vdict = dict_from_text(text, regex_list)
        vdict['filename'] = [file.split(os.path.sep)[-1]] * len(vdict['value'])
        df = df.append(vdict,ignore_index=True)
    df.to_csv('extracted.csv', sep = ';')
    return df 

def text_check(text, regex_list): 
    '''
    input: text as string and list of regex expressions 
    output: highlighted text as string with color coding to terminal 
    '''
    htext = text #copy of highlighted text 
    for regex in regex_list:
        htext = re.sub(regex, Fore.RED + r'\1' + Fore.RESET, htext) # overwrite terminal output 
    return htext



if __name__ == "__main__":
    
    regex_list = [r'(p = \d+.\d+)',
                  r'(SD = \d+.\d+)'
                  r'(r = \d+.\d+)',
                  r'(p = .\d+)'
                  ]
    
    #=================================================#
    folderpath = '/Users/lukasmalik/Desktop/Masterarbeit/data/case_study/Stapel/unsuspicious'
    get_values(folderpath)
    
    
