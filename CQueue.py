from CResident import CResident
from typing import List, Any
from numpy import random

class CQueue(object):

    def __init__(self, max_people_in_queue:int, probabilities_to_stay:dict ):
        self.max_people_in_queue = max_people_in_queue
        self.curr_people_in_queue = 0
        self.probabilities_to_stay_per_amount_of_people = probabilities_to_stay
        self.time_per_amount_of_people = dict.fromkeys(range(max_people_in_queue),0)
        self.curr_service_time = 0
        self.wait_time_list = 0
        self.service_time_list = 0
        self.residents_queue:List[CResident] = []

    def decision(self, probability):
        return random.random() < probability

    def addResidentToTheQueue(self, resident:CResident)->bool:
        if(self.curr_people_in_queue == self.max_people_in_queue):
            return False

        probability = self.probabilities_to_stay_per_amount_of_people[self.curr_people_in_queue]
        stat = self.decision(probability)
        if( stat == False ):
            return False

        else:
            self.residents_queue.append(resident)
            self.curr_people_in_queue += 1
            return True

    def removeResidentFromTheQueue(self):
        resident = self.residents_queue[0]
        self.wait_time_list += resident.waiting_time
        self.service_time_list += resident.service_time
        self.residents_queue.remove(self.residents_queue[0])
        self.curr_people_in_queue -= 1

    def addWaitingTimeToResidents(self,time):
        for resident in self.residents_queue:
            resident.waiting_time += time



