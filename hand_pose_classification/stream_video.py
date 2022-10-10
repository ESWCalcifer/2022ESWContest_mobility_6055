from scene import Scene
from flask import Flask, send_from_directory
from flask_executor import Executor
from flask_cors import CORS
from bson.json_util import dumps
from pathlib import Path
app = Flask(__name__)
CORS(app)
c_scene = Scene()
executor = Executor(app)
@app.route('/job')
def index():
    while True:
        executor.submit(c_scene.start_loop())
@app.route('/scene')
def video_feed():
    return send_from_directory('gif',Path(c_scene.get_last_gif()))

@app.route("/get_first_camera", methods = ['GET'])
def get_first_camera():
    return dumps({'detected' : "True" if c_scene.is_exist() else "False"})

app.run(host='0.0.0.0', port='5000', debug=False)
