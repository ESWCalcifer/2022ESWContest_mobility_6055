# -*- coding: utf-8 -*-
from data_generate import num_hand
# import hand_detection_module
import cv2
from datetime import datetime
import paho.mqtt.client as mqtt
import imageio
class Scene():
    def __init__(self):
        self.image_lst = []
        self.cap_usb= cv2.VideoCapture(-1)
        self.message = str
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async("192.168.0.200",1883, 60)
        self.exist = False
        self.last_gif = str
        # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/home/pim/esw/test_mqtt/gesture")

        # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        self.message = str(msg.payload.decode("utf-8"))
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
            while self.message == "startsig":
                success_usb, frame_usb = self.cap_usb.read()
                image_lst.append(frame_usb)
        if self.message == "stopsig" and len(image_lst) is not 0:
            curr_time = datetime.now().strftime("%H%M%S")
            imageio.mimsave(f'./video_{curr_time}.gif', image_lst, fps = 10)
            self.last_gif = f"./video_{curr_time}.gif"
            cv2.imwrite(f"./frame_{curr_time}.jpg", frame_usb)
            image_lst = []
            self.exist = True

