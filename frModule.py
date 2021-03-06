import cv2
import face_recognition
import numpy as np
import os
import time
import dbModule as dbm
from sender import sendData


def determinating(encodeListKnown, classNames, recogniser, recognisers):
    time.sleep(2)

    people = {'name': [], 'status': []}

    while True:
        time.sleep(0.06)

        facePhotos, detectionTimes, statuses = dbm.selectBunch(recognisers)
        dbm.deleteBunch(recognisers)

        try:
            facePhoto, detectionTime, status = facePhotos[recogniser], detectionTimes[recogniser], statuses[recogniser]

            img = facePhoto

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            encodeCurFrame = face_recognition.face_encodings(img)

            for encodeFace in encodeCurFrame:
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, 0.5)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex]

                    if name not in people['name'] or\
                            status != people["status"][len(people["name"]) - people["name"][::-1].index(name) - 1]:
                        os.system(f'say -v Milena -r 2000 {name.split("_")[0]}')
                        people['name'].append(name)
                        people['status'].append(status)

                    sendData(name.split('_')[1], name.split('_')[0], detectionTime,
                             status, 'add')

        except:
            pass
