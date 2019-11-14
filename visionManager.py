import time


class Ozobot:
    waitingTime = 0

    def __init__(self, coords1, coords2, probabilityOfBeingReal):
        self.coords1 = coords1
        self.coords2 = coords2
        self.realness = probabilityOfBeingReal
        self.centerOfMass = (coords1[0] + ((coords2[0] - coords1[0]) / 2), coords1[1] + ((coords2[1] - coords1[1]) / 2))

    def startWaiting(self):
        self.waitingTime = time.time()

    def getWaitingTime(self):
        return time.time() - self.waitingTime


def getOzobotObjects(objs):
    ozobots = []
    for eachItem in objs:
        newOzobot = Ozobot(
            (eachItem["bp"][0], eachItem["bp"][1]),
            (eachItem["bp"][2], eachItem["bp"][3]),
            eachItem["prob"])
        ozobots.append(newOzobot)

    return ozobots
