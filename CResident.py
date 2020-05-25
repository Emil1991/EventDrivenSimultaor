class CResident(object):
    def __init__(self, service_time):
        self.waiting_time = 0
        self.service_time = service_time

    def addTimeInWaiting(self, time):
        self.waiting_time += time

    def addTimeInService(self, time):
        self.service_time += time
