from openvino_detection import video_detection
from flask import Flask, render_template, Response
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
import json
import cv2

app = Flask(__name__)
CORS(app)
detection = video_detection()
detection.get_frame()

client = MongoClient('localhost:27017')
db = client.video
collection = db.detection

def video_stream():
    while True:
        frame = detection.get_frame()
        ret, buffer = cv2.imencode('.jpeg',frame)
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@app.route('/')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/get_first_camera", methods = ['GET'])
def get_first_camera():
    try:
        first_detection = collection.find_one({"_id":"1"})
        return dumps(first_detection)
    except Exception as e:
        return dumps({'error' : str(e)})

# @app.route("/get_second_camera", methods = ['GET'])
# def get_second_camera():
#     try:
#         second_detection = collection.find_one({"_id":"2"})
#         return dumps(second_detection)
#     except Exception as e:
#         return dumps({'error' : str(e)})

app.run(host='0.0.0.0', port='5000', debug=False)