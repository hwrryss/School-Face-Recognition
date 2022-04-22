import sender


def getClassData():
    response = sender.sendData('', '', '', '', 'gather')
    data = []
    data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers = [], [], [], [], [], [], [], []

    for i in range(len(response)):
        data.append(response[i]['fields'])

    for i in range(len(data)):
        if data[i]['grade'] == 'Teacher':
            dataTeachers.append(data[i]['name'])

        if data[i]['grade'] == '10C':
            data10C.append(data[i]['name'])

        if data[i]['grade'] == '9C':
            data9C.append(data[i]['name'])

        if data[i]['grade'] == '8C':
            data8C.append(data[i]['name'])

        if data[i]['grade'] == '7C':
            data7C.append(data[i]['name'])

        if data[i]['grade'] == '6C':
            data6C.append(data[i]['name'])

        if data[i]['grade'] == '6T':
            data6T.append(data[i]['name'])

        if data[i]['grade'] == '5C':
            data5C.append(data[i]['name'])

    return data5C, data6C, data6T, data7C, data8C, data9C, data10C, dataTeachers
