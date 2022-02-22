import sqlite3
import cv2
import numpy as np
from datetime import datetime


con = sqlite3.connect('SFR.db')
cur = con.cursor()


def createTable():
    cur.execute("CREATE TABLE IF NOT EXISTS images(sub INTEGER NOT NULL UNIQUE, photo BLOB NOT NULL, time TEXT)")
    con.commit()


def insertImage(sub, photo):
    query = """ INSERT INTO images(sub, photo, time) VALUES (?, ?, ?)"""

    time = datetime.now().strftime("%H:%M:%S")
    blobPhoto = photo
    data = (sub, blobPhoto, time)

    cur.execute(query, data)
    con.commit()


def checkLength():
    query = """SELECT sub FROM images"""
    cur.execute(query)

    result = cur.fetchall()

    con.commit()

    return len(result)


def selectBunch():
    query = """SELECT photo,time FROM images WHERE sub > ? AND sub <= ?"""

    tsp = checkLength()
    data = (tsp - 1, tsp)

    cur.execute(query, data)
    result = cur.fetchall()

    detectionTimes = []
    facePhotos = []

    for i in range(len(result)):
        blobPhoto = result[i][0]
        blobPhoto = np.frombuffer(blobPhoto, np.byte)
        facePhotos.append(cv2.imdecode(blobPhoto, cv2.IMREAD_ANYCOLOR))

        detectionTimes.append(result[i][1])

    con.commit()

    return facePhotos, detectionTimes


def deleteBunch():
    query = """DELETE FROM images WHERE sub > ? AND sub <= ?"""

    tsp = checkLength()
    data = (tsp - 1, tsp)

    cur.execute(query, data)
