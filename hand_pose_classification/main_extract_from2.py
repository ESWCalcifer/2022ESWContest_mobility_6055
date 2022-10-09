# Programme core
# -*- coding: utf-8 -*-

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
from picamera.array import PiRGBArray
from picamera import PiCamera
import paho.mqtt.client as mqtt

model_name = 'hand_model.sav'

# custom function
def rps(num):
    if num == 0:
        return 'Start' #paper
    # elif num == 1:
    #     return 'GOOD'
    else:
        return 'End' #rock

font = cv2.FONT_HERSHEY_PLAIN
hands = hand_detection_module.HandDetector(max_hands=num_hand)
model = pickle.load(open(model_name, 'rb'))

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
#cv2.VideoCapture(-1, cv2.CAP_V4L)
cap_usb= cv2.VideoCapture(-1)
# datatype of output frame is np ndarray
# use print(type(cap_laptop))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

client = mqtt.Client()
# set callback function on_connect(connect to broker), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
# address : localhost, port: 1883 에 연결
client.connect('192.168.0.200', 1883)
client.loop_start()

sci = 0
# while cap_laptop.isOpened():
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # success_laptop, frame_laptop = cap_laptop.read()
    # # print(type(frame_laptop))
    # if not success_laptop:
    #     print("Ignoring empty camera frame.")
    #     continue
    # if success_laptop:
        
    image, my_list = hands.find_hand_landmarks(cv2.flip(frame.array, 1), draw_landmarks=False)
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
                    client.publish("/home/pim/esw/test_mqtt/gesture","startsig", 1)
                    print("startsig given")
                    curr_time = datetime.now().strftime("%H%M%S") 
                elif pred == "End":
                    client.publish("/home/pim/esw/test_mqtt/gesture","stopsig", 1)
                    print("stopsig given")
                    # cv2.imwrite("frame_%s.png" % (curr_time), frame_usb)
                # if pred == "GOOD":
                #     cap_laptop.release()
                #     cap_usb.release()
        sci += 1
                # cap_usb.release()
                # else:
                #     break
    rawCapture.truncate(0)
                
    cv2.imshow('Hands', image)
    # draw_text(frame_laptop, text, 30, 50)
    # cv2.imshow("Color", frame_laptop)

    cv2.waitKey(1)
    client.loop_stop()