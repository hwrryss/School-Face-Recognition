import sqlite3
import cv2
import numpy as np
from datetime import datetime
import threading


con = sqlite3.connect('SFR.db', check_same_thread=False)
cur = con.cursor()

lock = threading.Lock()

def createTable():
    cur.execute("CREATE TABLE IF NOT EXISTS images(sub INTEGER NOT NULL UNIQUE, photo BLOB NOT NULL, time TEXT)")
    con.commit()


def insertImage(photo):
    query = """ INSERT INTO images(sub, photo, time) VALUES (?, ?, ?)"""

    time = datetime.now().strftime("%H:%M:%S")
    blobPhoto = photo

    d = datetime.now()
    unixtime = d.microsecond

    data = (unixtime, blobPhoto, time)

    cur.execute(query, data)
    con.commit()


def selectBunch(recognisers):
    try:
        lock.acquire(True)
        query = """SELECT photo,time FROM images ORDER BY sub ASC LIMIT ?"""
        data = (recognisers, )

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

    finally:
        lock.release()


def deleteBunch(recognisers):
    query = """DELETE FROM images WHERE sub in (SELECT sub FROM images ORDER BY sub ASC LIMIT ?)"""
    data = (recognisers, )

    cur.execute(query, data)


def deleteAllImages():
    cur.execute("""DELETE FROM images""")
    con.commit()
