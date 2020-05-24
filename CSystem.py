from .demi import CQueue


class CSystem:
    queues = {}

    def __init__(self, T, M):
        self.timeUnitsPassed = 0
        self.numberOfStayed = 0
        self.numberOfLeft = 0
        self.simulationTime = T
        self.numberOfStations = M
        for i in range(M):
            self.queues[i] = CQueue()

    def getCurrentTime(self):
        return self.timeUnitsPassed

    def addTimeTicks(self, ticks):
        self.timeUnitsPassed += ticks

    def getNumberOfStayed(self):
        return self.numberOfStayed

    def getNumberOfLeft(self):
        return self.numberOfLeft

    def personStayed(self):
        self.numberOfStayed += 1

    def personLeft(self):
        self.numberOfStayed -= 1
