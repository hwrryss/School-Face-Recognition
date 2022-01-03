import cv2
import face_recognition
import numpy as np
import os
import sys
from datetime import datetime
import time
import gsModule
import rcModule
import cpModule


cpModule.cropPhotos()

path = 'samples'
images = []
classNames = []
myList = os.listdir(path)


for cl in myList:
    images.append(cv2.imread(f'{path}/{cl}'))
    classNames.append(os.path.splitext(cl)[0])

print(classNames)


def findEncoding(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncoding(images)

cap = cv2.VideoCapture(0)

pTime = 0

while True:
    now = datetime.now()

    if now.strftime('%H') == '22':
        rcModule.createReport()
        gsModule.clearGoogleSheet()
        sys.exit()

    success, img = cap.read()

    cTime = time.time()

    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name.split('_')[0], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            gsModule.editGoogleSheet(name.split('_')[0], name.split('_')[1])

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
