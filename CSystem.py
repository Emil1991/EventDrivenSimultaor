from CQueue import CQueue


class CSystem:
    queues = {}

    def __init__(self, T, M, probabilitySequnce:dict):
        self.timeUnitsPassed = 0
        self.numberOfStayed = 0
        self.numberOfLeft = 0
        self.simulationTime = T
        self.numberOfStations = M
        for i in range(M):
            self.queues[i+1] = CQueue(len(probabilitySequnce), probabilitySequnce)

    def getCurrentTime(self):
        return self.timeUnitsPassed

    def addTimeTicks(self, ticks):
        self.timeUnitsPassed += ticks

    def personStayed(self):
        self.numberOfStayed += 1

    def personLeft(self):
        self.numberOfStayed -= 1

    def getQueues(self):
        return self.queues

    #---------------------------OUTPUT---------------------------

    def getY(self):
        return self.numberOfStayed

    def getX(self):
        return self.numberOfLeft

    def getATI(self,i):
        return 0

    def getZI(self,i):
        return 0

    def getAW(self):
        return 0

    def getAS(self):
        return 0

    def getALambdaA(self):
        return 0

    def getOutput(self):
        getATIString=''

        for i in

        print("{0} {1} {2}")
