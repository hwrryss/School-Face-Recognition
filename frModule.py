import cv2
import face_recognition
import numpy as np
import time
import dbModule as dbm
from sender import sendData


def determinating(encodeListKnown, classNames, recogniser, recognisers):
    time.sleep(1)

    while True:
        time.sleep(0.5)

        facePhotos, detectionTimes, statuses = dbm.selectBunch(recognisers)
        dbm.deleteBunch(recognisers)

        try:
            facePhoto, detectionTime, status = facePhotos[recogniser], detectionTimes[recogniser], statuses[recognisers]

            img = facePhoto

            imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
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
                             status, 'add')


        except:
            pass
