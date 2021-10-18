import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions.drawing_styles import _THICKNESS_CONTOURS, _THICKNESS_DOT

cap = cv2.VideoCapture(0)

pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh 
faceMesh = mpFaceMesh.FaceMesh(min_detection_confidence = 0.01, min_tracking_confidence = 0.01)    # Передаются параметры: "Статичное изображение(T/F), Максималное кол-во лиц, 
                                    # минимальная уверенность для обнаруживания, минимальная уверенность для трекинга" (by default = False, 2, 0.5, 0.5)
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)   



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Перевод картинки из BGR в RGB
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks: 
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img,faceLms,mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)

        # for id, lm in enumerate(faceLms.landmark):
        #     h, w, c = img.shape # Высота, Ширина, Каналы
        #     cx, cy = int(lm.x * w), int(lm.y * h) # Определение координат на картинке


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}' , (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
