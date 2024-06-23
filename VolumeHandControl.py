import cv2
import time
import numpy as np
import HandTrackModule as htm
import math
import osascript

#
wCam, hCam = 640, 480
#
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.6)

osascript.osascript('get volume settings')
volResult = osascript.osascript('get volume settings')
print(volResult)
print(type(volResult))
volInfo = volResult[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
print(outputVol)

minVol = 0
maxVol = 100
target_volume = 100
osascript.osascript("set volume output volume {}".format(target_volume))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPostion(img, draw=False)
    if len(lmList) != 0: 
        print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand Range 25 - 130
        # Volume Range 0 - 100

        vol = np.interp(length, [25, 180], [minVol, maxVol])
        print(int(length), vol)
        osascript.osascript("set volume output volume {}".format(vol))

        if length < 25:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)