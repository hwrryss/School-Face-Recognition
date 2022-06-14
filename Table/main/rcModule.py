from datetime import date
import pandas as pd
import requests


def gatherInfo(data):
    data5C, data6C, data6T, data7C, data8C, data9C, data10C = [], [], [], [], [], [], []
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

    return data5C, data6C, data6T, data7C, data8C, data9C, data10C


def createReport(data):
    data5C, data6C, data6T, data7C, data8C, data9C, data10C = gatherInfo(data)

    today = date.today()

    d = {
        '5C': [i for i in data5C],
        '6C': [i for i in data6C],
        '6T': [i for i in data6T],
        '7C': [i for i in data7C],
        '8C': [i for i in data8C],
        '9C': [i for i in data9C],
        '10C': [i for i in data10C]
    }

    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()

    df.to_csv('./archive/' + 'stats' + str(today) + '.csv')


def sendForm(data, grade):
    st_url = 'https://docs.google.com/forms/d/e/'
    # id_f = '1FAIpQLSd-dqblh39ntn3Fe4_0lATKNp_384OhvNGhjdJvsOAYR_HYgQ'
    id_f = '1FAIpQLScNHiG8GGHqfyeWKIiPXGtt0LrL127FPwc72tW-W9OB9exbNQ'
    m_url = '/formResponse'
    sep = 'entry.'
    # id_is = [705137491, 1920121489, 1285254702, 1217149678, 405635450, 971565036, 1303487991, 1337446152, 127443765,
    #         243099865, 987548081, 156759101]
    id_is = [496933240, 700842451, 653673647, 1306825863, 1133370450, 1566678188, 585888123, 1224540757, 1426766905,
             1735568962, 1021354637, 53651792]
    answers = ['ул. Судакова, д.29', grade[:-1] + '-' + grade[-1]]

    quantities = {'attend': 0, 'absent': 0, 'unknown': 0, 'illness': 0, 'quarantine': 0, 'other': 0}
    names = {'unknown': [], 'illness': [], 'quarantine': [], 'other': []}

    for person in data:
        name, status, reason = person[0], person[1], person[2]

        if status != "Неизвестно":
            quantities['attend'] += 1

        else:
            if reason == 'Неизвестно':
                quantities['unknown'] += 1
                names['unknown'].append(name)

            if reason == 'Болеет':
                quantities['illness'] += 1
                names['illness'].append(name)

            if reason == 'Карантин':
                quantities['quarantine'] += 1
                names['quarantine'].append(name)

            if reason == 'Другое':
                quantities['other'] += 1
                names['other'].append(name)

            quantities['absent'] += 1

    answers.append(quantities['attend'])
    answers.append(quantities['absent'])

    answers.append(quantities['illness'])
    answers.append(', '.join(names['illness']) if 0 < len(names['illness']) < 10 else quantities['illness'])

    answers.append(quantities['quarantine'])
    answers.append(', '.join(names['quarantine']) if 0 < len(names['quarantine']) < 10 else quantities['quarantine'])

    answers.append(quantities['other'])
    answers.append(', '.join(names['other']) if 0 < len(names['other']) < 10 else quantities['other'])

    answers.append(quantities['unknown'])
    answers.append(', '.join(names['unknown']) if 0 < len(names['unknown']) < 10 else quantities['unknown'])

    url = st_url + id_f + m_url
    form_data = {sep + str(id_i): str(i) for id_i, i in zip(id_is, answers)}

    requests.post(url, data=form_data)
