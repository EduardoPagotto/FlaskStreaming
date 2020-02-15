#!/usr/bin/env python3
'''
Created on 20200202
Update on 20200214
@author: Eduardo Pagotto
'''
import time
from .base_camera import BaseCamera

import logging
import logging.config
import yaml
import queue

class Camera(BaseCamera):
    """[sequencia as imagens]
    Arguments:
        BaseCamera {[type]} -- [description]
    Returns:
        [type] -- [description]
    Yields:
        [type] -- [description]
    """

    queue_in = queue.Queue()
    queue_out = queue.Queue()

    config_file = './etc/FlaskStream.yaml' 
    appname = 'FlaskStreaming'
    last_image = 'empty_img.jpg'

    with open(config_file, 'r') as stream:
        global_config = yaml.load(stream)
        logging.config.dictConfig(global_config['loggin'])
        log = logging.getLogger(appname)
        log.info('>>>>>> Starting %s, loading setup file: %s',appname, config_file)

    @staticmethod
    def getNext():

        data = None
        for _ in range(5):
            if Camera.queue_in.empty() == False:

                image_name = Camera.queue_in.get(block=False)
                with open(image_name, 'rb') as file:
                    data = file.read()
                    Camera.last_image = image_name
                
                Camera.queue_out.put(image_name)

                return data
            else:
                time.sleep(1)

        # if (int(Camera.lastTimeHasAudience()) + 60) > int(time.time()):
        #     Camera.last_image = 'empty_img.jpg'

        with open(Camera.last_image, 'rb') as file:
            data = file.read()

        # with open("empty_img.jpg", 'rb') as file:
        #     data = file.read()

        return data     

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.getNext()
