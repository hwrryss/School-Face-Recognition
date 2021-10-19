import cv2
import numpy as np
import face_recognition

imgFirst = face_recognition.load_image_file('photos/DenisGood.jpg')
imgFirst = cv2.cvtColor(imgFirst, cv2.COLOR_BGR2RGB)

imgSecond = face_recognition.load_image_file('photos/Danya.jpg')
imgSecond = cv2.cvtColor(imgSecond, cv2.COLOR_BGR2RGB)

firstFaceLoc = face_recognition.face_locations(imgFirst)[0]
firstEncode = face_recognition.face_encodings(imgFirst)[0]
cv2.rectangle(imgFirst, (firstFaceLoc[3], firstFaceLoc[0]), (firstFaceLoc[1], firstFaceLoc[2]), (255, 0, 255), 2)

secondFaceLoc = face_recognition.face_locations(imgSecond)[0]
secondEncode = face_recognition.face_encodings(imgSecond)[0]
cv2.rectangle(imgSecond, (secondFaceLoc[3], secondFaceLoc[0]), (secondFaceLoc[1], secondFaceLoc[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([firstEncode], secondEncode)
faceDis = face_recognition.face_distance([firstEncode], secondEncode)
print(results, faceDis)

cv2.imshow('imgFirst', imgFirst)
cv2.imshow('imgSecond', imgSecond)
cv2.waitKey(0)
