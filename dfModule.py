import cv2
import mediapipe as mp
import sys
from datetime import datetime
import frModule
import dbModule as dbm
import sender
import asyncio


class FaceDetector:
    def __init__(self, minDetectionCon=0.7):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, status):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(imgRGB)

        if self.result.detections:
            for id, detection in enumerate(self.result.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape

                x1, y1, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                x2, y2 = x1 + w, y1 + h

                img = img[y1:y2, x1:x2]

                if len(img) != 0:
                    _, facePhoto = cv2.imencode('.jpg', img)
                    dbm.insertImage(facePhoto, status)


async def combining(encodeListKnown, classNames, recognisers):
    await asyncio.gather(
        *[asyncio.to_thread(frModule.determinating, encodeListKnown, classNames, recogniser, recognisers)
          for recogniser in range(recognisers)],
        *[asyncio.to_thread(startup, status) for status in ['Entered', 'Left']]
    )


def startup(status):
    cap = cv2.VideoCapture(1)

    if status == 'Left':
        cap = cv2.VideoCapture(0)

    detector = FaceDetector()

    while True:
        now = datetime.now()

        if now.strftime('%H') > '22':
            sender.sendData('', '', '', '', 'report')
            sender.sendData('', '', '', '', 'delete')
            dbm.deleteAllImages()
            sys.exit()

        success, img = cap.read()

        detector.findFaces(img, status)

        cv2.waitKey(1000)
