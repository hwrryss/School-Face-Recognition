import cv2
import face_recognition
import numpy as np
import time
import dbModule as dbm
from sender import sendData

import random


def determinating(encodeListKnown, classNames, recogniser, recognisers):
    time.sleep(0.5)

    while True:
        time.sleep(0.5)

        facePhotos, detectionTimes = dbm.selectBunch(recognisers)
        dbm.deleteBunch(recognisers)

        try:
            facePhoto, detectionTime = facePhotos[recogniser], detectionTimes[recogniser]

            img = facePhoto

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            encodeCurFrame = face_recognition.face_encodings(imgS)

            for encodeFace in encodeCurFrame:
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, 0.5)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex]

                    time.sleep(0.5)
                    sendData(name.split('_')[1], name.split('_')[0], detectionTime,
                             random.choice(['Entered', 'Left']), 'add')


        except:
            pass
