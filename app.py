#!/usr/bin/env python3
'''
Created on 20200202
Update on 20200215
@author: Eduardo Pagotto
'''

import time
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

import json

from FlaskStreaming.camera import Camera
from InvalidUsage import InvalidUsage

import threading

garbage_colector = None

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

        date = payload['date']
        print('Enqueued: ' + str(date))
        name_file = './imgs/{0}.jpg'.format(date)
        img = request.files['file']
        if img is not None:
          img.save(name_file)

        Camera.queue_in.put(name_file)

        return "ok"

    except Exception as exp:
        raise InvalidUsage('Falha Arquivo: {0}'.format(str(exp)), status_code=404)


@app.route('/hasAudienceNow', methods=['GET'])
def hasAudienceNow():

    if request.method == 'GET' is False:
        raise InvalidUsage('GET invalido', status_code=404)

    try:
        val = Camera.hasAudience()
        audience = {'hasAudience': val}

        return app.response_class(
            response=json.dumps(audience),
            status=200,
            mimetype='application/json'
        )

    except Exception as exp:
        raise InvalidUsage('GET: {0}'.format(str(exp)), status_code=404)

class GB():
    def __init__(self, queue_out):
        self.queue_out = queue_out

    def execute(self):
        print('gb online')
        while(True):
            try:
                if Camera.queue_out.empty() == False:
                    image_name = Camera.queue_out.get(block=False)
                    os.remove(image_name)
                    print('gb removeu:' + str(image_name))
                    time.sleep(1)
                    continue
                else:
                    time.sleep(15)
            except Exception as exp:
                print('gb erro critico: ' + str(exp))
                time.sleep(1)

@app.before_first_request
def execute_inicializacao():
    """[Inicaliza singleton do controle do scanner e batch]
    """
    global garbage_colector

    if garbage_colector is None:
        garbage_colector = GB(Camera.queue_out)
        thread1 = threading.Thread(target=garbage_colector.execute, name='gb_execute')
        thread1.setDaemon(True)
        thread1.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
