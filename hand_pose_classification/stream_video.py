from scene import Scene
from flask import Flask, Response, render_template
from flask_cors import CORS
from bson.json_util import dumps
app = Flask(__name__)
CORS(app)
scene = Scene()

def video_stream():
    while True:
        Scene().start_loop()
@app.route('/scene')
def video_feed():
    return dumps({'gifs' : Scene.get_last_gif()})

@app.route("/get_first_camera", methods = ['GET'])
def get_first_camera():
    return dumps({'detected' : "True" if Scene.is_exist() else "False"})

app.run(host='0.0.0.0', port='5000', debug=False)