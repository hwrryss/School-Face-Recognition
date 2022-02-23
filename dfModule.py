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

    def findFaces(self, img, draw=True):
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
                dbm.insertImage(facePhoto)


async def combining(encodeListKnown, classNames):
    await asyncio.gather(
        *[asyncio.to_thread(frModule.determinating, encodeListKnown, classNames, j)
          for j in range(1)],

        asyncio.to_thread(startup)
    )


def startup():
    cap = cv2.VideoCapture(0)

    detector = FaceDetector()

    while True:
        #print(time.strftime('%X'))
        last_time = time.time()
        now = datetime.now()

        if now.strftime('%H') > '22':
            rcModule.createReport()
            gsModule.clearGoogleSheet()
            dbm.deleteAllImages()
            sys.exit()

        success, img = cap.read()

        detector.findFaces(img)

        #print(f'detect - {time.time() - last_time}')

        cv2.waitKey(1000)
