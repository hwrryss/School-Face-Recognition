import cv2
import face_recognition
import os


def cropPhotos():
    path = 'samples'
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        images.append(cv2.imread(f'{path}/{cl}'))
        classNames.append(os.path.splitext(cl)[0])

    for className, img in zip(classNames, images):
        facesCurFrame = face_recognition.face_locations(img)

        for faceLoc in facesCurFrame:
            y1, x2, y2, x1 = faceLoc

            crop_img = img[y1:y2, x1:x2]

            cv2.imwrite(f"{path}/{className}.jpg", crop_img)
            cv2.waitKey(1)
