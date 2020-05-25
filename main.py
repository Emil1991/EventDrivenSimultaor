from CSystem import CSystem
from CQueue import CQueue
from CResident import CResident
import sys
import numpy as np

if __name__ == '__main__':

    #======== read the inputs from stdin ==========

    T = int(sys.argv[1])
    M = int(sys.argv[2])
    lamda = int(sys.argv[3])
    miu = int(sys.argv[4])
    probabilities = dict()

    i = 5
    while( i < len(sys.argv)):
        probabilities[i-5] = float(sys.argv[i])
        i += 1
    #==============================================

    system = CSystem(T,M,probabilities) #initial the System

    left_time = 0

    #========== resident arrival handling ==========
    while(True):
        arrived_time = np.random.poisson(lamda)
        left_time = T - system.timeUnitsPassed
        if(arrived_time > left_time):
            break
        system.addTimeTicks(arrived_time)
        chosenQueue = np.random.randint(1,3)
        systemQueues = system.queues

        service_time = np.random.poisson(miu)
        resident = CResident(service_time)


        for queue in system.queues:
            if(queue.curr_people_in_queue == 0):
                continue
            else:
                if(queue.curr_service_time > 0 and queue.curr_service_time<= arrived_time):
                    queue.removeResidentFromTheQueue()
                    queue.addWaitingTimeToResidents(queue.curr_service_time)
                    if (queue.curr_people_in_queue == 0):
                        continue
                time_to_add_from_last_iteration = queue.curr_service_time
                service_time = np.random.poisson(miu) ###############
                queue.curr_service_time = service_time
                service_time += time_to_add_from_last_iteration
                queue.residents_queue[0].service_time = queue.curr_service_time
                if (queue.curr_people_in_queue == 0):
                    continue
                while(service_time <= arrived_time):
                    queue.removeResidentFromTheQueue()
                    queue.addWaitingTimeToResidents(queue.curr_service_time)
                    if(queue.curr_people_in_queue == 0):
                        break
                    new_service_time = np.random.poisson(miu) ##########
                    queue.residents_queue[0].service_time = service_time
                    service_time += new_service_time + queue.curr_service_time
                if (queue.curr_people_in_queue == 0):
                    continue
                delta = service_time - arrived_time
                queue.curr_service_time = delta

        status = systemQueues[chosenQueue-1].addResidentToTheQueue(resident)
        if(status == False):
            system.numberOfLeft += 1
        else:
            system.numberOfStayed += 1

    #====================================================

    #= after stop arrivals, manage service time left (till T) in the queues =====
    maximum_time_left_in_queues = 0
    for queue in system.queues:
        if (queue.curr_people_in_queue == 0):
            continue
        else:
            if (queue.curr_service_time > 0 and queue.curr_service_time <= left_time):
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(queue.curr_service_time)
                if (queue.curr_people_in_queue == 0):
                    continue
            time_to_add_from_last_iteration = queue.curr_service_time
            service_time = np.random.poisson(miu)
            queue.curr_service_time = service_time
            service_time += time_to_add_from_last_iteration
            queue.residents_queue[0].service_time = queue.curr_service_time
            while (service_time <= left_time):
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(queue.curr_service_time)
                if (queue.curr_people_in_queue == 0):
                    continue
                service_time = np.random.poisson(miu)
                queue.residents_queue[0].service_time = service_time
                service_time += service_time + queue.curr_service_time
            delta = service_time - left_time
            queue.curr_service_time = delta
    #===========================================================

    #== after stop arrivals, finish with the residents who still inside the queues ====
    for queue in system.queues:
        queue_time_till_empty=0
        if (queue.curr_people_in_queue == 0):
            continue
        else:
            if (queue.curr_service_time > 0):
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(queue.curr_service_time)
                queue_time_till_empty += queue.curr_service_time
            while(queue.curr_people_in_queue > 0):
                service_time = np.random.poisson(miu)
                queue.curr_service_time = service_time
                queue_time_till_empty += service_time
                queue.residents_queue[0].service_time = queue.curr_service_time
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(queue.curr_service_time)
            if(queue_time_till_empty > maximum_time_left_in_queues):
                maximum_time_left_in_queues = queue_time_till_empty
    #=====================================================================================

    #================== prints outputs ==============================
    system.ALamdaA = system.timeUnitsPassed / system.numberOfStayed
    system.addTimeTicks(maximum_time_left_in_queues+left_time)
    print(system.numberOfStayed, system.numberOfLeft, system.timeUnitsPassed, system.getAW(), system.getAS(), system.getALambdaA())
    print(iterations_number)
    #=================================================================