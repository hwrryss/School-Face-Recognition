import csv
from datetime import date
import gsModule


def createReport():
    data5C, data6C, data6T, data7C, data8C, data9C, data10C = gsModule.getClassData()
    today = date.today()

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
