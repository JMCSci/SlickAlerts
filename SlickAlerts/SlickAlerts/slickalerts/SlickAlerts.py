''' SlickAlerts 
    For now, only checks four keywords, case sensitive
    Will add an data structure so that an unlimited amount of keywords can be used
'''
from asyncio.tasks import sleep

''' exit program when 15 second alert ends '''

import datetime
import requests
import time
import math
from playsound import playsound

def main():
    programTitle()
    pageNumber = 0
    inStock = False
    start = True 
    restart = True

    while(restart):
        try:
            sleepDuration = (eval(input("Enter time interval (in minutes): ")))   # time between each scan
            if(sleepDuration < 0):
                sleepDuration = sleepDuration * -1
            keywords = input("Enter keywords (separated by a space): ")     # add keywords to list data structure
            words = keywords.split()
            keywordList = [str(x) for x in words]   # list that contains all keywords
            pagesToCheck = eval(input("Enter the total number of pages to check: "))       # total pages to check for keywords 
            if(pagesToCheck < 0):
                pagesToCheck = pagesToCheck * -1
            newLine()
            restart = False
        except NameError:
            print("Please enter a valid number.\n")
            restart = True
        except SyntaxError:
            print("Please enter a valid number.\n")
            restart = True
        
    
    # if keywordsList is empty exit program
    if(len(keywordList) == 0):
        start = False
        print("You have not entered any keywords. The program will exit.")
    
    while(start):
        inStock, pageNumber, start, item = readPage(keywordList, pagesToCheck, start)
        if(inStock == True):
            checkStock(inStock, pageNumber, item)
        else:
            checkPage(pageNumber, pagesToCheck, sleepDuration)
            
# programTitle: Prints program title            
def programTitle(): 
    print("*----------------------------------------*")
    print("|                                        |")
    print("|              SLICKALERTS               |")
    print("|                                        |")
    print("*----------------------------------------*\n")

# newLine: Prints a new line
def newLine():
    print()
            
# readPage: Reads and scans HTML page for keywords
def readPage(keywordList, pagesToCheck, start):
    pageNumber = 1     
    keywordsConcat = ""
    
    # Concatenate keywords
    for i in keywordList:
            keywordsConcat += i + " "

    while(pageNumber <= pagesToCheck):
        request = requests.get("https://slickdeals.net/forums/forumdisplay.php?f=9&page=" + str(pageNumber))
        print("SCANNING PAGE...DONE")
        # iterate through list
        for i in keywordList:
            # Separate if statements to return which one was found
            if(i.upper() in request.text.upper()):
                inStock = True
                start = False
                request.close()
                return inStock, pageNumber, start, i
            else:
                pageNumber += 1
                inStock = False
        # check concatenated keywords 
        if(keywordsConcat.upper() in request.text.upper()):
                inStock = True
                start = False
                request.close()
                return inStock, pageNumber, start, keywordsConcat
        request.close()        
    return inStock, pageNumber, start, None

# checkPage: Checks to see if past page -- reset back to page one and waits 15 minutes
def checkPage(pageNumber, pagesToCheck, sleepDuration):    
    if(pageNumber > pagesToCheck):
        pageNumber = 1
        currentTime = datetime.datetime.now();
        print(currentTime)
        print("Not found")
        if(sleepDuration == 1):
            print("Waiting " + str(sleepDuration) + " minute\n")
        else:
            print("Waiting " + str(sleepDuration) + " minutes\n")
        sleepDuration = sleepDuration * 60  # convert to seconds
        time.sleep(sleepDuration)
        
# checkStock: Prints message and plays alert if found
def checkStock(inStock, pageNumber, item):
    if(inStock == True):
        # Play audio alert
        currentTime = datetime.datetime.now();
        print(currentTime)
        print(item.capitalize() + " found")
        print("Slickdeals page:",pageNumber)
        playsound("/Users/jasonmoreau/Desktop/alert.mp3")
       
if __name__ == '__main__':
    main()