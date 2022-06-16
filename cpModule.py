import cv2
import face_recognition
import os


def cropPhotos():
    path = 'samples'
    images = []
    classNames = []
    myList = os.listdir(path)

    if '.DS_Store' in myList:
        os.system("rm -rf samples/.DS_Store")
        myList.remove(".DS_Store")

    for cl in myList:
        images.append(cv2.imread(f'{path}/{cl}'))
        classNames.append(os.path.splitext(cl)[0])

    for className, img in zip(classNames, images):
        facesCurFrame = face_recognition.face_locations(img)

        if facesCurFrame:
            for faceLoc in facesCurFrame:
                y1, x2, y2, x1 = faceLoc

                decreased = (y2 - y1)*(x2 - x1)/20000
                y1 = y1 - decreased if y1 > decreased else 0
                x1 = x1 - decreased if x1 > decreased else 0
                y2 = y2 + decreased if y2 + decreased < img.shape[0] else img.shape[0]
                x2 = x2 + decreased if x2 + decreased < img.shape[1] else img.shape[1]

                crop_img = img[int(y1):int(y2), int(x1):int(x2)]

                try:
                    check_facesCurFrame = face_recognition.face_encodings(crop_img)[0]

                    cv2.imwrite(f"{path}/{className}.jpg", crop_img)
                    cv2.waitKey(1)

                except:
                    pass

        else:
            os.system(f'rm "{path}/{className}.jpg"')
