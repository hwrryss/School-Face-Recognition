import cv2
import face_recognition
import numpy as np
import time
import gsModule
import dbModule as dbm


def determinating(encodeListKnown, classNames, j):
    time.sleep(0.5)

    while True:
        time.sleep(0.5)

        facePhotos, detectionTimes = dbm.selectBunch()
        dbm.deleteBunch()

        try:
            facePhoto, detectionTime = facePhotos[j], detectionTimes[j]

            img = facePhoto

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            encodeCurFrame = face_recognition.face_encodings(imgS)

            for encodeFace in encodeCurFrame:
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, 0.5)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()

                    last_time = time.time()

                    time.sleep(0.5)

                    gsModule.editGoogleSheet(name.split('_')[0], name.split('_')[1], detectionTime)

        except:
            pass
