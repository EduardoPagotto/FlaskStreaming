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

class Camera(BaseCamera):
    """[sequencia as imagens]
    Arguments:
        BaseCamera {[type]} -- [description]
    Returns:
        [type] -- [description]
    Yields:
        [type] -- [description]
    """

    tot_imges = 0

    config_file = './etc/FlaskStream.yaml' 
    appname = 'FlaskStreaming'

    last = 0
    ultima = 0

    with open(config_file, 'r') as stream:
        global_config = yaml.load(stream)
        logging.config.dictConfig(global_config['loggin'])
        log = logging.getLogger(appname)
        log.info('>>>>>> Starting %s, loading setup file: %s',appname, config_file)

        tot_imges = global_config[appname]['total']
        delay = global_config[appname]['delay']

    imgs = []
    for i in range(tot_imges):
        imgs.append('./imgs/{0}.jpg'.format(i))

    @staticmethod
    def getNext():
        reload = False
        while(True):
            try:
                novo = int(time.time() % Camera.delay) # nova a cada 3 segundos
                if novo == 0 or reload is True:
                    reload = False
                    Camera.ultima = Camera.last % Camera.tot_imges
                    Camera.last += 1

                prox = Camera.imgs[Camera.ultima]
                print('Show: {0}'.format(prox))
                #print('Novo:{0} Last:{1} Ultima:{2} img:{3}'.format(str(novo), str(Camera.last),str(Camera.ultima), str(prox)))
                with open(prox, 'rb') as file:
                    data = file.read()
                    return data
            except:
                Camera.last = 0
                reload = True
                continue

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.getNext()
