import operator


class Process:
    def __init__(self, id, length):
        self.id = id
        self.length = length
        self.timeProcessed = 0
        self.timeWaiting = 0
        self.timeToProcess = -1

    def process(self, timeSlice):
        self.timeProcessed += timeSlice
        if self.timeProcessed > self.length:
            self.timeProcessed = self.length
        return (self.length-self.timeProcessed)

    def wait(self, timeProcessed):
        self.timeWaiting += timeProcessed

    def finish(self):
        self.timeToProcess = self.timeProcessed + self.timeWaiting

    def reset(self):
        self.timeWaiting = 0
        self.timeProcessed = 0
        self.timeToProcess = 0


class Scheduler:
    def __init__(self):
        self.readyProcesses = []
        self.doneProcesses = []
        self.currentProcessCounter = 0
        self.readyProcessCount = 0

    def __str__(self):
        output = "---------------------------\nProcese pregatite:"
        for process in self.readyProcesses:
            output += "\nProces " + str(process.id) + ": [lungime: " + str(process.length) + ", timp de procesare: " + str(
                process.timeProcessed) + ", timp de asteptare: " + str(process.timeWaiting) + ", timp procesat: " + str(process.timeToProcess) + "]"
        output += "\nProcese terminate:"
        for process in self.doneProcesses:
            output += "\nProces " + str(process.id) + ": [lungime: " + str(process.length) + ", timp de procesare: " + str(
                process.timeProcessed) + ", timp de asteptare: " + str(process.timeWaiting) + ", timp procesat: " + str(process.timeToProcess) + "]"
        output += "\n---------------------------"
        return output

    def addProcess(self, processLength):
        self.readyProcesses.append(
            Process(self.readyProcessCount, processLength))
        self.readyProcessCount += 1

    def _transitionProcess(self, process):
        self.doneProcesses.append(process)
        self.readyProcesses.remove(process)
        self.readyProcessCount -= 1
        self.currentProcessCounter -= 1
        process.finish()

    def _waitOtherProcesses(self, waitTime, currentProccess):
        for process in self.readyProcesses:
            if process != currentProccess:
                process.wait(waitTime)

    def sortDoneByProcessId(self):
        self.doneProcesses.sort(key=operator.attrgetter('id'))

    def sortReadyByProcessId(self):
        self.readyProcesses.sort(key=operator.attrgetter('id'))

    def reset(self):
        for process in self.doneProcesses:
            self.readyProcesses.append(process)
        for process in self.readyProcesses:
            process.reset()
        self.sortReadyByProcessId()
        self.doneProcesses.clear()
        self.readyProcessCount = len(self.readyProcesses)
        self.currentProcessCounter = 0

    def totalWaitTime(self):
        totalWaitTime = 0
        for process in self.doneProcesses:
            totalWaitTime += process.timeWaiting
        return totalWaitTime

    def averageWaitTime(self):
        return self.totalWaitTime()/len(self.doneProcesses)

    def totalProcessingTime(self):
        totalProcessingTime = 0
        for process in self.doneProcesses:
            totalProcessingTime += process.timeToProcess
        return totalProcessingTime

    def averageProcessingTime(self):
        return self.totalProcessingTime() / len(self.doneProcesses)

    def _RR_process(self, timeSlice, printEachRound):
        processTimeRemaining = 0
        waitTime = 0
        currentProcess = None

        while (len(self.readyProcesses) > 0):
            if self.currentProcessCounter == self.readyProcessCount:
                self.currentProcessCounter = 0

            currentProcess = self.readyProcesses[self.currentProcessCounter]
            processTimeRemaining = currentProcess.process(timeSlice)

            if processTimeRemaining <= 0:
                self._transitionProcess(currentProcess)

            waitTime = timeSlice if processTimeRemaining >= 0 else timeSlice + processTimeRemaining
            self._waitOtherProcesses(waitTime, currentProcess)

            self.currentProcessCounter += 1

            if printEachRound:
                print(self)

    def _FCFS_process(self, printEachRound):
        currentProcess = None

        while (len(self.readyProcesses) > 0):
            currentProcess = self.readyProcesses[0]
            self.readyProcesses[0].process(currentProcess.length)
            self._transitionProcess(currentProcess)
            self._waitOtherProcesses(currentProcess.length, currentProcess)            
            
            if printEachRound:
                print(self)


    def schedule(self, method, timeSlices, printEachRound):
        if method == "RR":
            self._RR_process(timeSlices, printEachRound)
        elif method == "FCFS":
            self._FCFS_process(printEachRound)
