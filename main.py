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
        parameterLamda = 1/lamda
        arrived_time = np.random.exponential(parameterLamda)
        left_time = T - system.timeUnitsPassed

        if(arrived_time > left_time):
            break

        system.addTimeTicks(arrived_time)
        chosenQueue = np.random.randint(1,M+1)

        parameterMiu = 1/miu
        service_time = np.random.exponential(parameterMiu)
        resident = CResident(service_time)



        for queue in system.queues:
            if(queue.curr_people_in_queue == 0):
                continue
            else:
                if(queue.residents_queue[0].service_time > 0 and queue.residents_queue[0].service_time > arrived_time):
                    queue.residents_queue[0].service_time -= arrived_time
                    waiting_time = arrived_time
                    i=1
                    while(i<queue.curr_people_in_queue):
                        queue.residents_queue[i].waiting_time += waiting_time
                        i += 1
                    continue
                time_to_add_from_last_iteration = queue.residents_queue[0].service_time
                if(queue.residents_queue[0].service_time > 0 and queue.residents_queue[0].service_time <= arrived_time):
                    waiting_time = queue.residents_queue[0].service_time
                    queue.removeResidentFromTheQueue()
                    queue.addWaitingTimeToResidents(waiting_time)
                    if (queue.curr_people_in_queue == 0):
                        continue
                # service_time = np.random.poisson(miu)
                # queue.curr_service_time = service_time
                # service_time += time_to_add_from_last_iteration
                # queue.residents_queue[0].service_time = queue.curr_service_time
                if (queue.curr_people_in_queue == 0):
                    continue
                while(queue.residents_queue[0].service_time + time_to_add_from_last_iteration <= arrived_time):
                    time_to_add_from_last_iteration = queue.residents_queue[0].service_time + time_to_add_from_last_iteration
                    waiting_time = queue.residents_queue[0].service_time
                    queue.removeResidentFromTheQueue()
                    queue.addWaitingTimeToResidents(waiting_time)
                    if(queue.curr_people_in_queue == 0):
                        break
                if (queue.curr_people_in_queue == 0):
                    continue
                delta = (queue.residents_queue[0].service_time + time_to_add_from_last_iteration) - arrived_time
                queue.residents_queue[0].service_time = delta

        status = system.queues[chosenQueue-1].addResidentToTheQueue(resident)
        if(status == False):
            system.numberOfLeft += 1
            # print(system.queues[chosenQueue-1].curr_people_in_queue)
        else:
            system.numberOfStayed += 1
            system.queues[chosenQueue - 1].service_time_list += resident.service_time
    #====================================================

    #= after stop arrivals, manage service time left (till T) in the queues =====
    maximum_time_left_in_queues = 0
    for queue in system.queues:
        if (queue.curr_people_in_queue == 0):
            continue
        else:
            if (queue.residents_queue[0].service_time > 0 and queue.residents_queue[0].service_time > left_time):
                queue.residents_queue[0].service_time -= left_time
                waiting_time = left_time
                i = 1
                while (i < queue.curr_people_in_queue):
                    queue.residents_queue[i].waiting_time += waiting_time
                    i += 1
                continue
            time_to_add_from_last_iteration = queue.residents_queue[0].service_time
            if (queue.residents_queue[0].service_time > 0 and queue.residents_queue[0].service_time <= left_time):
                waiting_time = queue.residents_queue[0].service_time
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(waiting_time)
                if (queue.curr_people_in_queue == 0):
                    continue
            # service_time = np.random.poisson(miu)
            # queue.curr_service_time = service_time
            # service_time += time_to_add_from_last_iteration
            # queue.residents_queue[0].service_time = queue.curr_service_time
            if (queue.curr_people_in_queue == 0):
                continue
            while (queue.residents_queue[0].service_time + time_to_add_from_last_iteration <= left_time):
                time_to_add_from_last_iteration = queue.residents_queue[0].service_time + time_to_add_from_last_iteration
                waiting_time = queue.residents_queue[0].service_time
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(waiting_time)
                if (queue.curr_people_in_queue == 0):
                    break
            if (queue.curr_people_in_queue == 0):
                continue
            delta = (queue.residents_queue[0].service_time + time_to_add_from_last_iteration) - left_time
            queue.residents_queue[0].service_time = delta
    #===========================================================

    #== after stop arrivals, finish with the residents who still inside the queues ====
    for queue in system.queues:
        queue_time_till_empty=0
        if (queue.curr_people_in_queue == 0):
            continue
        else:
            if (queue.residents_queue[0].service_time > 0):
                queue_time_till_empty += queue.residents_queue[0].service_time
                waiting_time = queue.residents_queue[0].service_time
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(waiting_time)
            while(queue.curr_people_in_queue > 0):
                # service_time = np.random.poisson(miu)
                # queue.curr_service_time = service_time
                queue_time_till_empty += queue.residents_queue[0].service_time
                # queue.residents_queue[0].service_time = queue.curr_service_time
                waiting_time = queue.residents_queue[0].service_time
                queue.removeResidentFromTheQueue()
                queue.addWaitingTimeToResidents(waiting_time)
            if(queue_time_till_empty > maximum_time_left_in_queues):
                maximum_time_left_in_queues = queue_time_till_empty
    #=====================================================================================

    #================== prints outputs ==============================
    system.ALamdaA = system.timeUnitsPassed / system.numberOfStayed
    system.addTimeTicks(maximum_time_left_in_queues+left_time)
    print(system.numberOfStayed, system.numberOfLeft, system.timeUnitsPassed, system.getAW(), system.getAS(), system.ALamdaA)
    #=================================================================