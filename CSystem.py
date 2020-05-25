from CQueue import CQueue


class CSystem:
    queues = []

    def __init__(self, T, M, probabilitySequnce:dict):
        self.timeUnitsPassed = 0
        self.numberOfStayed = 0
        self.numberOfLeft = 0
        self.simulationTime = T
        self.numberOfStations = M
        self.ALamdaA = 0
        for i in range(M):
            self.queues.append(CQueue(len(probabilitySequnce), probabilitySequnce))

    def getCurrentTime(self):
        return self.timeUnitsPassed

    def addTimeTicks(self, ticks):
        self.timeUnitsPassed += ticks

    def personStayed(self):
        self.numberOfStayed += 1

    def personLeft(self):
        self.numberOfStayed -= 1


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
        total_waiting_time = 0
        for queue in self.queues:
            total_waiting_time += queue.wait_time_list
        return float(total_waiting_time / self.numberOfStayed)

    def getAS(self):
        total_service_time = 0
        for queue in self.queues:
            total_service_time += queue.service_time_list
        return float(total_service_time / self.numberOfStayed)

    def getALambdaA(self):
        return 0

    def getOutput(self):
        print("{0} {1} {2}")
