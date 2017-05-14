#!/usr/bin/env python
import sys
from collections import OrderedDict


# Read all URLs or IP address from file into list
def readURLListFile(URLList_File): 
    try:
        fileHandler = open(URLList_File,"r")
        fileList = fileHandler.readlines() # read file into a list with \n
        return fileList
    except IOError as e:
        print (e) #Does not exist OR no read permissions
        sys.exit(0) # Exit 
    finally:
        fileHandler.close()   
        
# get unique list of URLs or IP address
def getUniqueURLList(fileList):
    # Weed out blank lines with filter and return as list
    fileList = filter(lambda x: not x.isspace(), fileList)
    #from collections import OrderedDict    
    uniqueURLList = OrderedDict.fromkeys(fileList) # remove duplicates and return as list 
    return uniqueURLList.keys()   

'''
before each data print, we will move the cursor back to the beginning of the current line, 
cut out the entire line of text, and then print our current bit of data.
this will print data to the same line of the terminal. 
'''
def dynamicPrinter(data):
    sys.stdout.write("\r\x1b[K"+data.__str__())
    sys.stdout.flush()
    sys.stderr.flush()      