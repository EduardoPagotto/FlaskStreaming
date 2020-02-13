#!/usr/bin/env python3
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

import json

# import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
from FlaskStreaming.camera import Camera
from InvalidUsage import InvalidUsage

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/newzzxxccA1', methods=['POST'])
def newzzxxccA1():

    if request.method != 'POST':
        raise InvalidUsage('Invalido', status_code=404)

    try:
        s_payload = request.form['json']
        s_json_payload = s_payload.replace("'", "\"")
        payload = json.loads(s_json_payload)

        name = payload['img']
        img = request.files['file']
        if img is not None:
            img.save(name)

        return "ok"

    except Exception as exp:
        raise InvalidUsage('Falha Arquivo: {0}'.format(str(exp)), status_code=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
