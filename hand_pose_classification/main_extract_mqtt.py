# -*- coding: utf-8 -*-
import imp
import re
from unicodedata import bidirectional
from id_distance import calc_all_distance
import pickle
from data_generate import num_hand
# import hand_detection_module
import cv2
import sys
import argparse
from datetime import datetime
import time

import paho.mqtt.client as mqtt


# cap_usb= cv2.VideoCapture(-1)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/home/pim/esw/test_mqtt/gesture")
sci = 0
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cap_usb= cv2.VideoCapture(-1)
    success_usb, frame_usb = cap_usb.read()
    if cap_usb.isOpened():
        # print(sci)
        if (sci % 6000): # 15000~30000이면 1초에 약 1~2장 찍힘
            if str(client.on_
            message) == "startsig":
                print('AY')
                # if (index % 1000 == 0):
                    # cap_usb.set(cv2.CAP_PdROP_POS_MSEC,(index*1000))
                curr_time = datetime.now().strftime("%H%M%S") 
                cv2.imwrite("./frame_%s.bmp" % (curr_time), frame_usb)
                if not cv2.imwrite("./frame_%s.bmp" % (curr_time), frame_usb):
                    raise Exception("can't write image")
    sci += 1
    print("no") #msg.topic+" "+str(msg.payload))
    # return str(msg.payload)

client = mqtt.Client()
# Client(client_id="pi2", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.200", 1883, 60)
# client.loop_start()
# print(success_usb)
# print(cap_usb.isOpened())
sci += 1
if cap_usb.isOpened():
    print(sci)
    if (sci % 6000): # 15000~30000이면 1초에 약 1~2장 찍힘
        
        if str(client.on_message) == "startsig":
            print('AY')
                # if (index % 1000 == 0):
                    # cap_usb.set(cv2.CAP_PdROP_POS_MSEC,(index*1000))
            curr_time = datetime.now().strftime("%H%M%S") 
            cv2.imwrite("./frame_%s.bmp" % (curr_time), frame_usb)
            if not cv2.imwrite("./frame_%s.bmp" % (curr_time), frame_usb):
                raise Exception("can't write image")
                # if pred == "GOOD":
                #     cap_laptop.release()
                #     cap_usb.release()
    
                # cap_usb.release()
                # else:
                #     break

# client.loop_stop()
client.loop_forever()