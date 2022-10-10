from scene import Scene
from flask import Flask, send_from_directory
from flask_executor import Executor
from flask_cors import CORS
from bson.json_util import dumps
from pathlib import Path
from datetime import datetime
import imageio
import paho.mqtt.client as mqtt
from data_generate import num_hand
import hand_detection_module
import cv2
app = Flask(__name__)
CORS(app)
c_scene = Scene()
executor = Executor(app)
global message
message = str
global last_gif
last_gif = str
global exists
exists = False
image_lst = []
cap_usb= cv2.VideoCapture(-1)
message = str

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/home/pim/esw/test_mqtt/gesture")
sci = 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global message
    message = str(msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("192.168.0.200",1883, 60)
def job():
    client.loop_start()
    if cap_usb.isOpened():
        success_usb, frame_usb = cap_usb.read()
        if message == "startsig":
            image_lst.append(frame_usb)
            # curr_time = datetime.now().strftime("%H%M%S%f")[:-1] 
            # cv2.imwrite("./frame_%s.png" % (curr_time), frame_usb)
            # if not cv2.imwrite("./frame_%s.png" % (curr_time), frame_usb):
            #     raise Exception("can't write image")
            image = frame_usb
    if message == "stopsig" and len(image_lst) is not 0:
        curr_time = datetime.now().strftime("%H%M%S")
        imageio.mimsave(f'./video_{curr_time}.gif', image_lst, fps = 10)
        cv2.imwrite(f"./frame_{curr_time}.jpg", frame_usb)
        last_gif = f'./video_{curr_time}.gif'
        image_lst = []

@app.route('/job')
def index():
    while True:
        executor.submit(job())
@app.route('/scene')
def video_feed():
    return send_from_directory('gif',Path(last_gif))

@app.route("/get_first_camera", methods = ['GET'])
def get_first_camera():
    return dumps({'detected' : "True" if exists else "False"})

app.run(host='0.0.0.0', port='5000', debug=False)
