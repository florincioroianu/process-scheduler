import scheduler
import sys

#In acest program am implementat atat metoda "First Come First Served" cat si "Round Robin"
#Pentru a rula programul, folositi comanda [python run.py] si introduceti lungimile proceselor, cand doriti sa incheiati procesul de introducere, introduceti o valoare negativa.

def userInput(prompt):
    userInput = input(prompt)
    if userInput == "exit":
        sys.exit()
    return userInput


def getProcessLengths(scheduler):
    print("Acesta este un simulator pentru studiul planificatorului de procese, va rog sa introduceti lungimile proceselor. Introduceti un numar negativ pentru a va opri")
    processLength = 0
    while processLength > -1:
        prompt = "Proces " + str(scheduler.readyProcessCount) + ": "
        try:
            processLength = int(userInput(prompt))
            if processLength > 0:
                scheduler.addProcess(processLength)
                print(scheduler)
            elif processLength == 0:
                print("Procesul nu poate avea lungime 0")
            elif scheduler.readyProcessCount < 1:
                processLength = 0
                print("Este nevoie de cel putin 1 proces")

        except TypeError:
            print("Nu ati introdus un numar, tastati exit pentru iesire")
        except ValueError:
            print("Nu ati introdus un numar, tastati exit pentru iesire")

    print(scheduler)


def getSchedulingMethod():
    schedulingMethods = [["FCFS", "First Come First Served"],["RR","Round Robin"]]

    print("Metode de planificare:\n---------------------------")
    for method in schedulingMethods:
        print(method[0]+" = "+method[1])
    print("---------------------------")

    schedulingMethod = "notSpecified"
    while schedulingMethod == "notSpecified":
        schedulingMethod = userInput("Introduceti metoda de planificare dorita: ").upper()
        if schedulingMethod == "RR":
            return schedulingMethod
        elif schedulingMethod=="FCFS":
            return schedulingMethod
        else:
            print("Metoda invalida, tastati exit pentru iesire.")
            schedulingMethod = "notSpecified"


def getTimeSlice():
    timeSlice = 0
    while timeSlice == 0:
        try:
            timeSlice = int(userInput("Introduceti lungimea cuantei de timp: "))
            if timeSlice > 0:
                return timeSlice
            else:
                print("Intervalul nu poate fi mai putin de 1, tastati exit pentru iesire.")
                timeSlice = 0
        except TypeError:
            print("Nu ati introdus un numar, tastati exit pentru iesire")
        except ValueError:
            print("Nu ati introdus un numar, tastati exit pentru iesire")

def getPrintEachStep():
    recievedInput = False

    while recievedInput == False:
        printEachStep = userInput("Doriti printarea fiecarui pas al planificatorului? Y/N: ").upper()
        if printEachStep == "Y":
            recievedInput = True
        elif printEachStep == "N":
            recievedInput = True
        else:
            print("Input invalid, tastati exit pentru iesire")
    
    return True if printEachStep == "Y" else False

def runSchedule():
    timeSlice = -1
    schedulingMethod = getSchedulingMethod()
    if schedulingMethod != ("FCFS"):
        timeSlice = getTimeSlice()
    printEachStep = getPrintEachStep()
    
    scheduler.schedule(schedulingMethod,timeSlice,printEachStep)

    print("\n---------------------------\nFinal:\n" +str(scheduler))
    print("Timpi de așteptare:\n---------------------------\nTimp total de asteptare: "+ str(scheduler.totalWaitTime()) + "\nTimp mediu de asteptare: " + str(scheduler.averageWaitTime()) + "\n---------------------------")
    print("Timpi de procesare:\n---------------------------\nTimp total de procesare: "+ str(scheduler.totalProcessingTime()) + "\nTimp mediu de procesare: " + str(scheduler.averageProcessingTime()) + "\n---------------------------")

def finishedOptions(scheduler):
    startAgain = False
    while not startAgain:
        print("Optiuni:\n---------------------------\nexit - inchidere program\nreset - se pastreaza procesele, astfel poti incerca alta metoda sau interval de timp(Round Robin)\nsort - se sorteaza coada cu procese finalizate dupa id\n---------------------------")
        option = userInput("").lower()

        if option == ("reset"):
            scheduler.reset()
            print(scheduler)
            startAgain = True
        elif option == "sort":
            scheduler.sortDoneByProcessId()
            print(scheduler)
        else:
            print("Optiune invalida, tastati exit pentru iesire")
    
    return False
            
stop = False
scheduler = scheduler.Scheduler()
getProcessLengths(scheduler)

while not stop :
    runSchedule()
    stop = finishedOptions(scheduler)


