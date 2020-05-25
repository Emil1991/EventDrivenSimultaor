from CQueue import CQueue


class CSystem:
    queues = []

    def __init__(self, T, M, probabilitySequnce:dict):
        self.timeUnitsPassed = 0
        self.numberOfStayed = 0
        self.numberOfLeft = 0
        self.simulationTime = T
        self.numberOfStations = M
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

    def getATI(self):
        Ati_list = []
        i = 0
        while(i <= self.queues[0].max_people_in_queue):
            Ati_list.append(0)
            i += 1
        for queue in self.queues:
            i = 0
            while(i <= queue.max_people_in_queue):
                Ati_list[i] += queue.time_per_amount_of_people[i]
                i += 1
        i = 0
        while (i <= queue.max_people_in_queue):
            Ati_list[i] = Ati_list[i] / self.numberOfStations
            i += 1
        return Ati_list

    def getZI(self):
        list = []
        i = 0
        while(i <= self.queues[0].max_people_in_queue):
            list.append(0)
            i += 1

        Ati = self.getATI()
        i = 0
        while (i < len(list)):
            list[i] = Ati[i] / self.timeUnitsPassed
            i += 1
        return list

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
        total_avg = 0
        for queue in self.queues:
            total_avg += queue.total_residents / queue.arrivals_time
        return total_avg / self.numberOfStations

