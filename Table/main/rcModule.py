from datetime import date
import pandas as pd


def gatherInfo(data):
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = [], [], [], [], [], [], [], []
    table = pd.DataFrame(data.values()).to_dict(orient="list")

    for i in range(len(table['name'])):
        if table['grade'][i] == '5C' and table['name'][i] not in data5C:
            data5C.append(table['name'][i])

        if table['grade'][i] == '6C' and table['name'][i] not in data6C:
            data6C.append(table['name'][i])

        if table['grade'][i] == '6T' and table['name'][i] not in data6T:
            data6T.append(table['name'][i])

        if table['grade'][i] == '7C' and table['name'][i] not in data7C:
            data7C.append(table['name'][i])

        if table['grade'][i] == '8C' and table['name'][i] not in data8C:
            data8C.append(table['name'][i])

        if table['grade'][i] == '9C' and table['name'][i] not in data9C:
            data9C.append(table['name'][i])

        if table['grade'][i] == '10C' and table['name'][i] not in data10C:
            data10C.append(table['name'][i])

        if table['grade'][i] == 'Teachers' and table['name'][i] not in dataTeachers:
            dataTeachers.append(table['name'][i])

    return data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers


def createReport(data):
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = gatherInfo(data)

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

    df.to_csv('./archive/' + 'stats' + str(today) + '.csv')
