'''
Created on 20180713
Update on 20200111
@author: Eduardo Pagotto
'''

from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        return rv