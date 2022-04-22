from datetime import date
import pandas as pd
import tgModule


def createReport():
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = tgModule.getClassData()

    today = date.today()

    d = {
        '5C': [i for i in data5C],
        '6C': [i for i in data6C],
        '6T': [i for i in data6T],
        '7C': [i for i in data7C],
        '8C': [i for i in data8C],
        '9C': [i for i in data9C],
        '10C': [i for i in data10C],
        'Teachers': [i for i in dataTeachers]
    }

    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()

    df.to_csv('Attendance/' + 'stats' + str(today) + '.csv')
