from bs4 import BeautifulSoup
import pathlib
import re
import pandas as pd
import glob,os
from functions import *   # This is the functions.py file present in the spazer folder. This file contains many functions that are used in this code. 
space_gained = 0
space_input = 0


path = "input/*.html"
    
for filename in glob.glob(path):
#for x in range(11):
    #filename = str(x) + ".html"
    file = pathlib.Path(filename)
    if (file.exists()):
        #Read each file
        f = open(filename, 'r', errors="ignore")
        contents = f.read()   
        
        #Remove html tags
        soup = BeautifulSoup(contents, 'lxml')        
        output = soup.get_text() 
        

        keywords_load()
        output = strip(output)
        pos =  parse(output)
        output = trim(output,pos)


        
        #Write the output variable contents to output/ folder.
        fw = open('output/' + filename.replace('input/',''), "w")
        fw.write(output)
        fw.close()
        f.close()
        
        #Calculate space savings
        space_input = space_input + len(contents)
        space_gained = space_gained + len(contents) - len(output)        

print("Total Space Gained = " + str(round(space_gained*100/space_input, 2)) + "%") 
