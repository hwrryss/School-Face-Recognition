import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import googleapiclient.discovery

path = 'determinating_photos'
images = []
classNames = []
myList = os.listdir(path)

crr_row = 2

for cl in myList:
    images.append(cv2.imread(f'{path}/{cl}'))
    classNames.append(os.path.splitext(cl)[0])


def editGoogleSheet(name):
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '11k5_jgmYdJNwUJcA_rx3IobWZB-WYl9koJogkNODPRU'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')

    values = (
        (name, dtString),
    )

    values_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    data = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:A1000',
        majorDimension='ROWS'
    ).execute()

    crr_row = len(data['values']) + 1

    if [name, ] not in data['values']:
        res = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range='A' + str(crr_row),
            body=values_range_body
        ).execute()


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
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            editGoogleSheet(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
