from datetime import date
import gsModule
import pandas as pd


def createReport():
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = gsModule.getClassData()

    today = date.today()

    d = {
        '5C': [i for i in set(sum(data5C['values'], []))] if data5C.get('values', False) != False else [],
        '6C': [i for i in set(sum(data6C['values'], []))] if data6C.get('values', False) != False else [],
        '6T': [i for i in set(sum(data6T['values'], []))] if data6T.get('values', False) != False else [],
        '7C': [i for i in set(sum(data7C['values'], []))] if data7C.get('values', False) != False else [],
        '8C': [i for i in set(sum(data8C['values'], []))] if data8C.get('values', False) != False else [],
        '9C': [i for i in set(sum(data9C['values'], []))] if data9C.get('values', False) != False else [],
        '10C': [i for i in set(sum(data10C['values'], []))] if data10C.get('values', False) != False else [],
        'Teachers': [i for i in set(sum(dataTeachers['values'], []))] if dataTeachers.get('values',
                                                                                          False) != False else []
    }

    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()

    df.to_csv('Attendance/' + 'stats' + str(today) + '.csv')
