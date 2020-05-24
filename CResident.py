class CResident(object):
    def __init__(self):
        self.waiting_time = 0;
        self.service_time = 0;

    def addTimeInWaiting(self, time):
        self.waiting_time += time

    def addTimeInService(self, time):
        self.service_time += time
