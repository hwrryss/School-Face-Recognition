import cv2
import mediapipe as mp
import sys
import time
from datetime import datetime
import gsModule
import rcModule
import frModule
import dbModule as dbm
import asyncio


class FaceDetector:
    def __init__(self, minDetectionCon=0.8):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, i, last_time, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(imgRGB)

        if self.result.detections:
            for id, detection in enumerate(self.result.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape

                x1, y1, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                x2, y2 = x1 + w, y1 + h

                img = img[y1:y2, x1:x2]

                _, facePhoto = cv2.imencode('.jpg', img)
                dbm.insertImage(i, facePhoto)

                i += 1

                last_time = time.time()

        return last_time, i


async def transfer(encodeListKnown, classNames, facePhotos, detectionTimes):
    await asyncio.gather(*[
        asyncio.to_thread(frModule.determinating, encodeListKnown, classNames, facePhotos[j], detectionTimes[j])
        for j in range(len(facePhotos))
    ])


def startup(encodeListKnown, classNames):
    dbm.createTable()

    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    last_time = time.time()

    i = dbm.checkLength() + 1

    time.sleep(1)

    while True:
        now = datetime.now()

        if now.strftime('%H') == '22':
            rcModule.createReport()
            gsModule.clearGoogleSheet()
            sys.exit()

        success, img = cap.read()

        last_time, i = detector.findFaces(img, i, last_time)

        print(time.time() - last_time)

        if time.time() - last_time > 3:
            facePhotos, detectionTimes = dbm.selectBunch()
            dbm.deleteBunch()

            i -= len(facePhotos)

            asyncio.run(transfer(encodeListKnown, classNames, facePhotos, detectionTimes))

            # for j in range(len(facePhotos)):
            #    frModule.determinating(encodeListKnown, classNames, facePhotos[j], detectionTimes[j])

        cv2.waitKey(300)
