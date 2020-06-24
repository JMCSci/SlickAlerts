''' SlickAlerts 
    For now, only checks four keywords, case sensitive
    Will add an data structure so that an unlimited amount of keywords can be used
'''


''' convert the text as it is scanned into all cap '''
''' this way you dont have to make it case sensitive '''

import datetime
import requests
import time
from playsound import playsound

def main():
    pageNumber = 0
    inStock = False
    start = True
    
    programTitle()
    
    sleepDuration = eval(input("Enter time interval (in minutes): "))
    keyword1, keyword2, keyword3, keyword4 = input("Enter 4 keywords (separated by comma then space): ").split(', ')
    pagesToCheck = eval(input("Enter the total number of pages to check: "))
    newLine()
    
    while(start):
        inStock, pageNumber, start = readPage(keyword1, keyword2, keyword3, keyword4, pagesToCheck, start)
        if(inStock == True):
            checkStock(inStock, pageNumber)
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
def readPage(keyword1, keyword2, keyword3, keyword4, pagesToCheck, start):
    pageNumber = 1
    
    while(pageNumber <= pagesToCheck):
        request = requests.get("https://slickdeals.net/forums/forumdisplay.php?f=9&page=" + str(pageNumber))
        print("SCANNING PAGE...DONE")
        # Separate if statements to return which one was found
        
        
        if(keyword1 in request.text or keyword2 in request.text \
           or keyword3 in request.text or keyword4 in request.text):            
            inStock = True
            start = False
            return inStock, pageNumber, start
        else:
            pageNumber += 1
            inStock = False
        
    return inStock, pageNumber, start

# checkPage: Checks to see if past page -- reset back to page one and waits 15 minutes
def checkPage(pageNumber, pagesToCheck, sleepDuration):    
    if(pageNumber > pagesToCheck):
        pageNumber = 1
        currentTime = datetime.datetime.now();
        print(currentTime)
        print("Not in stock")
        if(sleepDuration == 1):
            print("Waiting " + str(sleepDuration) + " minute\n")
        else:
            print("Waiting " + str(sleepDuration) + " minutes\n")
        sleepDuration = sleepDuration * 60  # convert to seconds
        time.sleep(sleepDuration)
        
# checkStock: Prints message and plays alert if found
def checkStock(inStock, pageNumber):
    if(inStock == True):
        # Play audio alert
        currentTime = datetime.datetime.now();
        print(currentTime)
        print("Slickdeals page:",pageNumber)
        playsound("/Users/jasonmoreau/Desktop/alert.mp3")
       
if __name__ == '__main__':
    main()