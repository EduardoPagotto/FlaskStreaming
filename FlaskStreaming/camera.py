import time
from .base_camera import BaseCamera

import logging
import logging.config
import yaml

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    #imgs = [open('./imgs/' + f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    tot_imges = 0

    config_file = './etc/FlaskStream.yaml' 
    appname = 'FlaskStreaming'

    with open(config_file, 'r') as stream:
        global_config = yaml.load(stream)
        logging.config.dictConfig(global_config['loggin'])
        log = logging.getLogger(appname)
        log.info('>>>>>> Starting %s, loading setup file: %s',appname, config_file)

        tot_imges = global_config[appname]['total']

    imgs = []
    for i in range(tot_imges):
        imgs.append('./imgs/{0}.jpg'.format(i))

    @staticmethod
    def getNext():
        prox = Camera.imgs[int(time.time()) % 3]
        with open(prox, 'rb') as file:
            data = file.read()
            return data

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.getNext()
