import face_recognition
import cv2
import asyncio
import os
from datetime import datetime
import cpModule
import dfModule
import dbModule as dbm

cpModule.cropPhotos()

dbm.createTable()

path = 'samples'
images = []
classNames = []
myList = os.listdir(path)


for cl in myList:
    images.append(cv2.imread(f'{path}/{cl}'))
    classNames.append(os.path.splitext(cl)[0])


def findEncoding(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncoding(images)

while True:
    now = datetime.now()

    if 22 > int(now.strftime('%H')) > 7:
        asyncio.run(dfModule.combining(encodeListKnown, classNames))
