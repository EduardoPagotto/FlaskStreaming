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

        novo = time.time() % 3 # nova a cada 3 segundos
        val = int(novo) % Camera.tot_imges

        prox = Camera.imgs[val]
        with open(prox, 'rb') as file:
            data = file.read()
            return data

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.getNext()
