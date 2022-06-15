import csv


def parseStudents():
    with open('./archive/toparse.csv', mode='r', encoding="utf8") as inp:
        reader = csv.reader(inp)
        everyone = [[rows[0], " ".join(rows[1:])] for rows in reader]

    return everyone
