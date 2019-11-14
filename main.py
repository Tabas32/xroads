import time

from customVideoDetector import *
from semaphoreControler import *
from visionManager import *

model_path = "detection_model45.h5"
json_path = "detection_config.json"

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = setUpNN(model_path, json_path)
client = setUpMqtt()
lastSemChange = 0
globalNorthLane = []
globalEastLane = []
globalSouthLane = []
globalWestLane = []
while(True):
    ret, frame = cap.read()

    output_img, detections = detect(detector, np.asarray(frame))
    all_objs = getObjects(detections, 'ozobot')

    ozobots = getOzobotObjects(all_objs)

# ---------------------- COUNTING --------------------------
    xc = -40  # Bulgarian constant
    yc = 40  # Georgian constant
    startOfImage = (0, 0)
    endOfImage = (1280, 720)
    centerOfImage = (startOfImage[0] + (endOfImage[0] - startOfImage[0]) / 2,
                     startOfImage[0] + (endOfImage[1] - startOfImage[1]) / 2)
    lengthOfLane = 1 * (endOfImage[1]) / 3
    northStart = (centerOfImage[0] - lengthOfLane / 4 + xc, centerOfImage[1] - lengthOfLane + yc)
    northEnd = (centerOfImage[0] + xc, centerOfImage[1] - lengthOfLane / 4 + yc)
    eastStart = (centerOfImage[0] + lengthOfLane / 4 + xc, centerOfImage[1] - lengthOfLane / 4 + yc)
    eastEnd = (centerOfImage[0] + lengthOfLane + xc, centerOfImage[1] + yc)
    southStart = (centerOfImage[0] + xc, centerOfImage[1] + lengthOfLane / 4 + yc)
    southEnd = (centerOfImage[0] + lengthOfLane / 4 + xc, centerOfImage[1] + lengthOfLane + yc)
    westStart = (centerOfImage[0] - lengthOfLane + xc, centerOfImage[1] + yc)
    westEnd = (centerOfImage[0] - lengthOfLane / 4 + xc, centerOfImage[1] + lengthOfLane / 4 + yc)

    northLane = []
    eastLane = []
    southLane = []
    westLane = []

    for ozokot in ozobots:
        if northStart[0] < ozokot.centerOfMass[0] < northEnd[0] and northStart[1] < ozokot.centerOfMass[1] < northEnd[
            1]:
            northLane.append(ozokot)

        elif eastStart[0] < ozokot.centerOfMass[0] < eastEnd[0] and eastStart[1] < ozokot.centerOfMass[1] < eastEnd[1]:
            eastLane.append(ozokot)

        elif southStart[0] < ozokot.centerOfMass[0] < southEnd[0] \
                and southStart[1] < ozokot.centerOfMass[1] < southEnd[1]:
            southLane.append(ozokot)

        elif westStart[0] < ozokot.centerOfMass[0] < westEnd[0] and westStart[1] < ozokot.centerOfMass[1] < westEnd[1]:
            westLane.append(ozokot)

    diffNorth = len(globalNorthLane) - len(northLane)
    if diffNorth < 0 and len(northLane) > 0:
        for i in range(abs(diffNorth)):
            northLane[len(northLane) - i - 1].startWaiting()
            globalNorthLane.append(northLane[len(northLane) - i - 1])
    elif diffNorth > 0:
        for i in range(diffNorth):
            try:
                globalNorthLane.pop(0)
            except:
                continue

    diffEast = len(globalEastLane) - len(eastLane)
    if diffEast < 0 and len(eastLane) > 0:
        for i in range(abs(diffEast)):
            eastLane[len(eastLane) - i - 1].startWaiting()
            globalEastLane.append(eastLane[len(eastLane) - i - 1])
    elif diffEast > 0:
        for i in range(diffEast):
            try:
                globalEastLane.pop(0)
            except:
                continue

    diffSouth = len(globalSouthLane) - len(southLane)
    if diffSouth < 0 and len(southLane) > 0:
        for i in range(abs(diffSouth)):
            southLane[len(southLane) - i - 1].startWaiting()
            globalSouthLane.append(southLane[len(southLane) - i - 1])
    elif diffSouth > 0:
        for i in range(diffSouth):
            try:
                globalSouthLane.pop(0)
            except:
                continue

    diffWest = len(globalWestLane) - len(westLane)
    if diffWest < 0 and len(westLane) > 0:
        for i in range(abs(diffWest)):
            westLane[len(westLane) - i - 1].startWaiting()
            globalWestLane.append(westLane[len(westLane) - i - 1])
    elif diffWest > 0:
        for i in range(diffWest):
            try:
                globalWestLane.pop(0)
            except:
                continue

# ------------------------------END OF COUNTING --------------------------------
    northTotalWaitingTime = 0
    eastTotalWaitingTime = 0
    southTotalWaitingTime = 0
    westTotalWaitingTime = 0

    for ozokot in globalNorthLane:
        northTotalWaitingTime += ozokot.getWaitingTime()
    for ozokot in globalEastLane:
        eastTotalWaitingTime += ozokot.getWaitingTime()
    for ozokot in globalSouthLane:
        southTotalWaitingTime += ozokot.getWaitingTime()
    for ozokot in globalWestLane:
        westTotalWaitingTime += ozokot.getWaitingTime()

    status = [northTotalWaitingTime, eastTotalWaitingTime, southTotalWaitingTime, westTotalWaitingTime]

    # status = [len(northLane), len(eastLane), len(westLane), len(southLane)]
    #print(getDirection(0) + " : " + status[0])
    #print(getDirection(1) + " : " + status[1])
    #print(getDirection(2) + " : " + status[2])
    #print(getDirection(3) + " : " + status[3])
    print(status)

    now = time.time()
    if now - lastSemChange > 10:
        lastSemChange = time.time()
        sendComand(client, status)

    cv2.circle(frame, (190, 160), 15, (255, 0, 0), -1)
    cv2.circle(frame, (1064, 642), 15, (255, 0, 0), -1)
    cv2.rectangle(frame, (int(northStart[0]), int(northStart[1])), (int(northEnd[0]), int(northEnd[1])), (50, 168, 109),
                  2)
    cv2.rectangle(frame, (int(eastStart[0]), int(eastStart[1])), (int(eastEnd[0]), int(eastEnd[1])), (50, 168, 109), 2)
    cv2.rectangle(frame, (int(southStart[0]), int(southStart[1])), (int(southEnd[0]), int(southEnd[1])), (50, 168, 109),
                  2)
    cv2.rectangle(frame, (int(westStart[0]), int(westStart[1])), (int(westEnd[0]), int(westEnd[1])), (50, 168, 109), 2)

    cv2.imshow("img", markObjectsCV(frame, all_objs))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
