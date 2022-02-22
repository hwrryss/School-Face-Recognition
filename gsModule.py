import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

crr_row = 2


def getClassData():
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '11k5_jgmYdJNwUJcA_rx3IobWZB-WYl9koJogkNODPRU'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

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

    dataTeachers = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='V2:V1000',
        majorDimension='ROWS'
    ).execute()

    return data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers


def editGoogleSheet(name, clas, dtString, crr_row=crr_row):
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
