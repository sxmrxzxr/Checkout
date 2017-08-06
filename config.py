'''
    config.py
    Configuration module for the server
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from uuid import uuid5, NAMESPACE_DNS
from socket import gethostname


class Config:
    def __init__(self):
        pass

    CLIENT_ID = uuid5(NAMESPACE_DNS, gethostname())
    VERSION = "1.0"
    AUTHOR = "Jake Lawrence"
    NAME = "Checkout"
    HOSTNAME = gethostname()

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    CONFIG_DIR = '/var/log/'
    LOGLEVEL = ''
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    SLACK_KEY = os.getenv('SLACK_KEY')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    ADMIN_EMAILS = ['tug64918@temple.edu']
    WELCOME_MSG = ['Welcome, ', 'Time to Hack, ', 'Hey there, ']

config = {
    'default': ProductionConfig
}
