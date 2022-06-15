import sqlite3
import cv2
import numpy as np
from datetime import datetime
import threading


con = sqlite3.connect('SFR.db', check_same_thread=False)
cur = con.cursor()

lock = threading.Lock()

def createTable():
    cur.execute("CREATE TABLE IF NOT EXISTS images(sub INTEGER NOT NULL UNIQUE,"
                " photo BLOB NOT NULL, time TEXT, status TEXT)")
    con.commit()


def insertImage(photo, status):
    try:
        lock.acquire(True)
        query = """ INSERT INTO images(sub, photo, time, status) VALUES (?, ?, ?, ?)"""

        time = datetime.now().strftime("%H:%M:%S")
        blobPhoto = photo

        d = datetime.now()
        unixtime = d.microsecond

        data = (unixtime, blobPhoto, time, status)

        cur.execute(query, data)
        con.commit()

    finally:
        lock.release()


def selectBunch(recognisers):
    try:
        lock.acquire(True)
        query = """SELECT photo,time,status FROM images ORDER BY sub ASC LIMIT ?"""
        data = (recognisers, )

        cur.execute(query, data)
        result = cur.fetchall()

        detectionTimes = []
        facePhotos = []
        statuses = []

        for i in range(len(result)):
            blobPhoto = result[i][0]
            blobPhoto = np.frombuffer(blobPhoto, np.byte)
            facePhotos.append(cv2.imdecode(blobPhoto, cv2.IMREAD_ANYCOLOR))

            detectionTimes.append(result[i][1])

            statuses.append(result[i][2])

        con.commit()

        return facePhotos, detectionTimes, statuses

    finally:
        lock.release()


def deleteBunch(recognisers):
    try:
        lock.acquire(True)
        query = """DELETE FROM images WHERE sub in (SELECT sub FROM images ORDER BY sub ASC LIMIT ?)"""
        data = (recognisers, )

        cur.execute(query, data)

    finally:
        lock.release()


def deleteAllImages():
    try:
        lock.acquire(True)
        cur.execute("""DELETE FROM images""")
        con.commit()

    finally:
        lock.release()
