from openvino_detection import video_detection
from flask import Flask, Response
from flask_cors import CORS
import sqlite3
from bson.json_util import dumps
import cv2

app = Flask(__name__)
CORS(app)
detection = video_detection()
detection.get_frame()
con = sqlite3.connect("video_db", check_same_thread=False)
cur = con.cursor()

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
        res = cur.execute("select detected from video where camera_id=0")
        string = res.fetchone()
        return dumps({'detected' : string[0]})
    except Exception as e:
        return dumps({'error' : str(e)})

# @app.route("/get_second_camera", methods = ['GET'])
# def get_second_camera():
#     try:
#         res = cur.execute("select detected from video where camera_id=1")
#         return dumps(res)
#     except Exception as e:
#         return dumps({'error' : str(e)})

app.run(host='0.0.0.0', port='5000', debug=False)