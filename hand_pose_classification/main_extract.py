# Programme core
import imp
import re
from unicodedata import bidirectional
from id_distance import calc_all_distance
import pickle
from data_generate import num_hand
import hand_detection_module
import cv2
import sys
import argparse
from datetime import datetime
import time


model_name = 'hand_model.sav'

# custom function
def rps(num):
    if num == 0:
        return 'Start'
    # elif num == 1:
    #     return 'GOOD'
    else:
        return 'End'

font = cv2.FONT_HERSHEY_PLAIN
hands = hand_detection_module.HandDetector(max_hands=num_hand)
model = pickle.load(open(model_name, 'rb'))

cap_laptop = cv2.VideoCapture(cv2.CAP_DSHOW)
cap_usb= cv2.VideoCapture(cv2.CAP_DSHOW+1)

sci = 0
while cap_laptop.isOpened():
    success_laptop, frame_laptop = cap_laptop.read()
    if not success_laptop:
        print("Ignoring empty camera frame.")
        continue
    if success_laptop:
        
        image, my_list = hands.find_hand_landmarks(cv2.flip(frame_laptop, 1), draw_landmarks=False)
        if my_list:
            height, width, _ = image.shape
            all_distance = calc_all_distance(height, width, my_list)
            pred = rps(model.predict([all_distance])[0])
            pos = (int(my_list[12][0]*height), int(my_list[12][1]*width))
            image = cv2.putText(image, pred, pos, font, 2, (0, 0, 0), 2)
            
            # image = cv2.putText(image, fps, (70, 70), font, 3, (0, 0, 0), 3)
            success_usb, frame_usb = cap_usb.read()
            if cap_usb.isOpened():
                if (sci % 6000): # 15000~30000이면 1초에 약 1~2장 찍힘
                    if pred == "Start":
                    # if (index % 1000 == 0):
                        # cap_usb.set(cv2.CAP_PdROP_POS_MSEC,(index*1000))
                        curr_time = datetime.now().strftime("%H%M%S") 
                        cv2.imwrite("frame_%s.png" % (curr_time), frame_usb)
                    # if pred == "GOOD":
                    #     cap_laptop.release()
                    #     cap_usb.release()
            sci += 1
                    # cap_usb.release()
                    # else:
                    #     break
                
    cv2.imshow('Hands', image)
    # draw_text(frame_laptop, text, 30, 50)
    # cv2.imshow("Color", frame_laptop)

    cv2.waitKey(1)
