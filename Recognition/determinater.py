import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime, date
import time
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import googleapiclient.discovery
import sys
import csv


path = 'determinating_photos'
images = []
classNames = []
myList = os.listdir(path)

crr_row = 2

for cl in myList:
    images.append(cv2.imread(f'{path}/{cl}'))
    classNames.append(os.path.splitext(cl)[0])


def get_data():
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '11k5_jgmYdJNwUJcA_rx3IobWZB-WYl9koJogkNODPRU'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

    today = date.today()

    data5C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:A1000',
        majorDimension='ROWS'
    ).execute()

    data6C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='D2:D1000',
        majorDimension='ROWS'
    ).execute()

    data6T = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='G2:G1000',
        majorDimension='ROWS'
    ).execute()

    data7C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='J2:J1000',
        majorDimension='ROWS'
    ).execute()

    data8C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='M2:M1000',
        majorDimension='ROWS'
    ).execute()

    data9C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='P2:P1000',
        majorDimension='ROWS'
    ).execute()

    data10C = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='S2:S1000',
        majorDimension='ROWS'
    ).execute()

    with open('stats' + str(today) + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(['5C'])
        spamwriter.writerow(i[0] for i in data5C['values'])

        spamwriter.writerow(['6C'])
        spamwriter.writerow(i[0] for i in data6C['values'])

        spamwriter.writerow(['6T'])
        spamwriter.writerow(i[0] for i in data6T['values'])

        spamwriter.writerow(['7C'])
        spamwriter.writerow(i[0] for i in data7C['values'])

        spamwriter.writerow(['8C'])
        spamwriter.writerow(i[0] for i in data8C['values'])

        spamwriter.writerow(['9C'])
        spamwriter.writerow(i[0] for i in data9C['values'])

        spamwriter.writerow(['10C'])
        spamwriter.writerow(i[0] for i in data10C['values'])


def clearGoogleSheet():
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '11k5_jgmYdJNwUJcA_rx3IobWZB-WYl9koJogkNODPRU'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

    res = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='A2:X1000'
    ).execute()


def editGoogleSheet(name, clas, crr_row=crr_row):
    if clas == 'Teacher':
        letter = 'V'
    else:
        if int(clas[0]) > 6 or clas[1] == 'T':
            clas = str(int(clas[0]) + 1) + clas[1]

        letter = chr(ord("A") + (int(clas[0]) - 5) * 3)

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
        (name, dtString, 'LEFT'),
    )

    values_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    data = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{letter}2:{letter}1000',
        majorDimension='ROWS'
    ).execute()

    data_entry = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{chr(ord(letter) + 2)}2:{chr(ord(letter) + 2)}1000',
        majorDimension='ROWS'
    ).execute()

    if 'values' in data:
        crr_row = len(data['values']) + 2

        if [name, ] in data['values']:
            if data_entry['values'][data['values'].index([name, ])] != [values[0][2], ]:
                res = service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    valueInputOption='USER_ENTERED',
                    range=letter + str(crr_row),
                    body=values_range_body
                ).execute()

        else:
            res = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                valueInputOption='USER_ENTERED',
                range=letter + str(crr_row),
                body=values_range_body
            ).execute()

    else:
        res = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range=letter + str(crr_row),
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
    now = datetime.now()

    if now.strftime('%H') == '22':
        get_data()
        clearGoogleSheet()
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

            editGoogleSheet(name.split('_')[0], name.split('_')[1])

    cv2.imshow('Webcam', img)
    cv2.waitKey(500)
