from dynamikontrol import Module
from cvzone.HandTrackingModule import HandDetector
import cv2
import math

LENGTH_THRESHOLD = 150

module = Module()

detector = HandDetector(detectionCon=0.8, maxHands=1)

cap = cv2.VideoCapture(0)

def draw_timeline(img, rel_x):
    img_h, img_w, _ = img.shape
    timeline_w = max(int(img_w * rel_x) - 50, 50)
    cv2.rectangle(img, pt1=(50, img_h - 50), pt2=(timeline_w, img_h - 48), color=(0, 0, 255), thickness=-1)

while cap.isOpened():
    ret, cam_img = cap.read()
    cam_img = cv2.flip(cam_img, 1)

    hands, cam_img = detector.findHands(cam_img)

    if hands:
        lm_list = hands[0]['lmList']

        length, _, cam_img = detector.findDistance(lm_list[4], lm_list[8], cam_img)

        if length < LENGTH_THRESHOLD:
            # angle between thumb and index finger
            angle = abs(math.degrees(math.atan2(lm_list[4][1] - lm_list[8][1], lm_list[4][0] - lm_list[8][0])))
            draw_timeline(cam_img, angle / 180)

            motor_angle = int(angle - 90)
            module.motor.angle(motor_angle, period=0.2)

            cv2.putText(cam_img, text='Angle %d' % (angle,), org=(w - 200, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(200, 10, 10), thickness=2)

    cv2.imshow('cam', cam_img)
    if cv2.waitKey(1) == ord('q'):
        break

module.disconnect()
