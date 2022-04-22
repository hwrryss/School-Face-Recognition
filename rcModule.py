from datetime import date
import pandas as pd
import tgModule


def createReport():
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = tgModule.getClassData()

    today = date.today()

    d = {
        '5C': [i for i in data5C] if data5C != False else [],
        '6C': [i for i in data6C] if data6C != False else [],
        '6T': [i for i in data6T] if data6T != False else [],
        '7C': [i for i in data7C] if data7C != False else [],
        '8C': [i for i in data8C] if data8C != False else [],
        '9C': [i for i in data9C] if data9C != False else [],
        '10C': [i for i in data10C] if data10C != False else [],
        'Teachers': [i for i in dataTeachers] if dataTeachers != False else []
    }

    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()

    df.to_csv('Attendance/' + 'stats' + str(today) + '.csv')
