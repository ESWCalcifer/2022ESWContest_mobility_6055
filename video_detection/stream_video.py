from openvino_detection import video_detection
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
detection = video_detection()
detection.get_frame()

def video_stream():
    while True:
        frame = detection.get_frame()
        ret, buffer = cv2.imencode('.jpeg',frame)
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port='5000', debug=False)