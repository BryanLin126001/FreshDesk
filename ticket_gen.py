import sys
import InitialUtil
import time
import Util
from DataValidateUtil import DataValidate
from Consumer import Customer
from Helpdesk import Freshdesk
from multiprocessing import Process, Queue 
import os


custQueue = Queue()
def IsCustomerPauseToCome():
    if Util.getRandomNumber(1,4) == 1:
        return True
    return False

def pauseCustomerToCome():
    if IsCustomerPauseToCome() == True:
        #time.sleep(Util.getPauseSecond())
        time.sleep(1)

def customerIsComing():
    custCount = 0
    numberOfCustomer = Util.getRandomNumber(0,6)
    while True:
        if custCount == numberOfCustomer:
            time.sleep(1)
        pauseCustomerToCome()
        cust = Customer()
        custQueue.put(cust)
        custCount += 1

def showHelp():
    print("\tticket_gen.py is to generate tickets randomly with random activities and store to a JSON file.\n\
    \targuments where:\n\
    \t\t-n\tThe number of tickets to generate\n\
    \t\t-o\tThe JSON file would store tickets activities information")

if __name__ == "__main__":
    validater = DataValidate()
    
    if validater.ValidateTimeFrames():
        if validater.ValidateSysArgsLengh(sys.argv) == True and validater.ValidateSysArgs(sys.argv) == True:
            
            ticketQuantity = int(sys.argv[2])
            outputFile = sys.argv[4]
            freshdesk = Freshdesk(ticketQuantity, outputFile)
            freshdesk.createTickets()           
            
            p = Process(target=customerIsComing, args=())
            p.start()

            while True:
                
                if(not custQueue.empty()):
                    freshdesk.serviceCustomer(custQueue.get())
                else:
                    continue
                
                if freshdesk.isTicketSoldOut():
                    print("ticket sold out")
                    break
                
                if validater.isGoingToClosed():
                    print("We are going to closed")
                    freshdesk.goingToClosed()
                    break

            p.terminate()
            freshdesk.generateTicketActivitiesDataList()
            wholeActivitiesDataDict = freshdesk.sortOutActivities()
            freshdesk.outputWholeTicketActivitiestoJsonFile(wholeActivitiesDataDict)
            print("Welcome to Freshdesk, see you later")
        elif sys.argv[1] == "--help":
            showHelp()
        else:
            print("Try 'python ticket_gen.py --help' for more information.")
    else:
        print("Sorry, we are not open.")