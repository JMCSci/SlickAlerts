''' SlickAlerts  '''

import datetime
import requests
import time
from playsound import playsound
from os.path import sys
import webbrowser as wb

def main():
    start = True
    inStock = False
    programTitle()
    instructions()
    pageNumber = 0
    sleepDuration, keywordList, pagesToCheck, openBrowser = settings()
    
    # If keywordsList is empty exit program
    if(len(keywordList) == 0):
        start = False
        print("You have not entered any keywords. The program will exit.")
    
    # Start scanning webpage after getting user settings
    while(start):
        inStock, pageNumber, start, item = readPage(keywordList, pagesToCheck, start)
        if(inStock == True):
            checkStock(inStock, pageNumber, item, openBrowser)
        else:
            checkPage(pageNumber, pagesToCheck, sleepDuration)
            
# programTitle: Prints program title            
def programTitle(): 
    print("*----------------------------------------*")
    print("|                                        |")
    print("|              SLICKALERTS               |")
    print("|                                        |")
    print("*----------------------------------------*\n")
    
    
def instructions():
    print("Instructions")
    print("------------")
    print("* Use hyphens to separate products that are phrases (ex: The-Last-Of-Us)")
    print("* Use spaces to separate products (ex: The-Last-Of-Us Honeywell Seagate)\n")
    

def settings():
    restart = True  # Initial settings for program
    while(restart):
        try:
            sleepDuration = (eval(input("Enter time interval (in minutes): ")))   # time between each scan
            if(sleepDuration < 0):
                sleepDuration = sleepDuration * -1
            keywords = input("Enter keywords (separated by a space): ")     # add keywords to list data structure
            words = keywords.split()
            keywordList = [str(x) for x in words]   # list that contains all keywords
            pagesToCheck = eval(input("Enter the total number of pages to check: "))   # total pages to check for keywords 
            if(pagesToCheck < 0):
                pagesToCheck = pagesToCheck * -1
            browserOption = input("Do you want to open a link to the webpage when found? Yes or No? ")
            browserOption = browserOption.upper()
            newLine()
            if(browserOption == "YES" or browserOption == "Y"):
                openBrowser = True
            else:
                openBrowser = False
            restart = False
        except NameError:
            print("Please enter a valid number.\n")
            restart = True
        except SyntaxError:
            print("Please enter a valid number.\n")
            restart = True
    return sleepDuration, keywordList, pagesToCheck, openBrowser
    

# newLine: Prints a new line
def newLine():
    print()
       
            
# readPage: Reads and scans HTML page for keywords
def readPage(keywordList, pagesToCheck, start):
    pageNumber = 1     

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
        pageNumber += 1
        inStock = False
        request.close()        
    return inStock, pageNumber, start, None

# checkPage: Checks to see if past page -- reset back to page one and waits 15 minutes
def checkPage(pageNumber, pagesToCheck, sleepDuration):    
    if(pageNumber > pagesToCheck):
        pageNumber = 1
        currentTime = datetime.datetime.now();
        newLine()
        print(currentTime)
        print("Not found")
        if(sleepDuration == 1):
            print("Waiting " + str(sleepDuration) + " minute\n")
        else:
            print("Waiting " + str(sleepDuration) + " minutes\n")
        sleepDuration = sleepDuration * 60  # convert to seconds
        time.sleep(sleepDuration)
        
# checkStock: Prints message and plays alert if found
def checkStock(inStock, pageNumber, item, openBrowser):
    if(inStock == True):
        # Play audio alert
        currentTime = datetime.datetime.now();
        newLine()
        print(currentTime)
        print("*** " + item.capitalize() + " found ***\n")
        print("Slickdeals page:",pageNumber)
        print("Your default web browser will now open.")
        playsound("alert.mp3")
        time.sleep(2)   # pause so user can read message
        if(openBrowser == True):
            wb.open("https://slickdeals.net/forums/forumdisplay.php?f=9&page=" + str(pageNumber)) # opens web browser when found
        sys.exit(-1)
        
       
if __name__ == '__main__':
    main()