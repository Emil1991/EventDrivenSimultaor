from CSystem import CSystem
from CQueue import CQueue
from CResident import CResident
import sys
import numpy as np

if __name__ == '__main__':
    # read the inputs from stdin
    T = int(sys.argv[1])
    M = int(sys.argv[2])
    lamda = int(sys.argv[3])
    miu = int(sys.argv[4])
    probabilities = dict()

    i = 5
    while( i < len(sys.argv)):
        probabilities[i-5] = float(sys.argv[i])
        i += 1

    system = CSystem(T,M,probabilities)

    while(True):
        arrived_time = np.random.poisson(lamda)
        system.addTimeTicks(arrived_time)
        chosenQueue = np.random.random_integers(1,M,1)[0]
        systemQueues = system.getQueues()
        resident = CResident()
        status = systemQueues[chosenQueue].addResidentToTheQueue(resident)
        if(status == False):
            system.numberOfLeft += 1
        else:
            system.numberOfStayed += 1

        for queue in system.getQueues():
            if(queue.curr_pepole_in_queue == 0):
                continue
            else:
                if(queue.curr_service_time > 0):
                    queue.removeResidentFromTheQueue()
                    queue.addTimeInService(queue.curr_service_time)
                time_to_add_from_last_iteration = queue.curr_service_time
                service_time = np.random.poisson(miu)
                queue.curr_service_time = service_time
                queue.getResidentsQueue()[0].service_time = queue.curr_service_time
                while(service_time + time_to_add_from_last_iteration <= arrived_time):
                    queue.removeResidentFromTheQueue()
                    queue.addTimeInService(queue.curr_service_time)
                    service_time = np.random.poisson(miu)
                    queue.getResidentsQueue()[0].service_time = service_time
                    service_time += service_time + queue.curr_service_time
                delta = service_time - arrived_time;
                queue.curr_service_time = delta
