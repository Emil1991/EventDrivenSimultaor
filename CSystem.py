class CSystem:
    queues = {}

    def __init__(self, M):
        for i in range(M):
            self.queues[i] = []
