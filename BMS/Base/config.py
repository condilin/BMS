# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: config.py
# @time: 19-6-11 上午11:58

import os
from flask_uploads import IMAGES


class Config:

    DEBUG = None
    SECRET_KEY = 'JfqhApfTNHFJbeRnxNtkC330B4Yp4Vyo1d74lKh19mX6NlqbgsVvrw=='

    # project base url
    PROJECT_BASE_URL = '/home/kyfq/MyPython/PycharmProjects/bms/BMS/Base'

    # sqlite uri
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(PROJECT_BASE_URL), 'bms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mongodb uri
    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_DBNAME = 'call_for_bids_old'
    MONGO_URI = 'mongodb://{}:{}/{}'.format(MONGO_HOST, MONGO_PORT, MONGO_DBNAME)

    # upload images config
    UPLOADED_IMG_ALLOW = IMAGES  # upload suffix which is allowed
    UPLOADED_IMG_DEST = os.path.join(PROJECT_BASE_URL, 'uploads/imgs/')  # save dst directory
    UPLOADED_IMG_URL = os.path.join(PROJECT_BASE_URL, 'uploads/imgs/')  # provide img url which is saved to user

    # upload file config
    UPLOADED_FILE_ALLOW = ('csv', 'xlsx', 'xls', 'txt')  # upload suffix which is allowed
    UPLOADED_FILE_DEST = os.path.join(PROJECT_BASE_URL, 'uploads/files/')  # save dst directory
    UPLOADED_FILE_URL = os.path.join(PROJECT_BASE_URL, 'uploads/files/')  # provide files url


# config of development
class DevelopConfig(Config):
    DEBUG = True


# config of production
class ProductConfig(Config):
    DEBUG = False


# mapping the config
project_config = {
    'development': DevelopConfig,
    'product': ProductConfig
}
