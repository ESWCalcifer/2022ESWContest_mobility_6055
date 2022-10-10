# -*- coding: utf-8 -*-
from data_generate import num_hand
# import hand_detection_module
# import cv2
from datetime import datetime
import paho.mqtt.client as mqtt
import imageio

class Scene():
    client = mqtt.Client()
    rc = 0

    def __init__(self):
        self.image_lst = []
        # self.cap_usb= cv2.VideoCapture(0)
        self.message = str
        self.exist = False
        self.last_gif = str
        # The callback for when the client receives a CONNACK response from the server.

    def is_exist(self):
        return self.exist
    def get_last_gif(self):
        if self.is_exist():
            return self.last_gif
        else:
            return None
    def start_loop(self):
        self.client.loop_start()
        if self.cap_usb.isOpened():
            if self.message == "startsig":
                success_usb, frame_usb = self.cap_usb.read()
                self.image_lst.append(frame_usb)
            if self.message == "stopsig" and len(self.image_lst) > 0:
                curr_time = datetime.now().strftime("%H%M%S")
                imageio.mimsave(f'./video_{curr_time}.gif', self.image_lst, fps = 10)
                self.last_gif = f"./video_{curr_time}.gif"
                cv2.imwrite(f"./frame_{curr_time}.jpg", frame_usb)
                self.image_lst = []
                self.exist = True
cscene = Scene()
