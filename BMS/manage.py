# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: manage.py
# @time: 19-7-18 下午4:30


# import sys
import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from Base.config import project_config, Config


# initial sqlalchemy object
db = SQLAlchemy()
# initial mongodb object
mongo_bids = PyMongo()
# create images object
images = UploadSet('img', IMAGES)
# create upload object
files = UploadSet('file', ('txt', 'csv', 'xls', 'xlsx'))
# login
login_manager = LoginManager()


# log configure
class ConfigLog(object):
    def __init__(self):
        self.log_name = os.path.join(Config.PROJECT_BASE_URL, 'logs/bms.log')
        self.log_format = '%(levelname)s [%(asctime)s] %(message)s'

        logging.basicConfig(
            level=logging.WARNING,
            format=self.log_format,
            filename=self.log_name,
        )


# factory mode
def create_app(config_name):

    app = Flask(__name__)

    # load config
    app.config.from_object(project_config[config_name])

    # relate between sqlite and app
    db.init_app(app)

    # relate between mongodb and app
    mongo_bids.init_app(app)

    # register UploadSet instances
    configure_uploads(app, files)
    configure_uploads(app, images)

    # relate between login and app
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'

    # register blueprint
    from DataShow import data_show_blue
    app.register_blueprint(data_show_blue)
    from URLSearch import url_search_blue
    app.register_blueprint(url_search_blue)
    from User import user_blue
    app.register_blueprint(user_blue)

    return app


# run
app = create_app('product')

# db migrate
Migrate(app, db)

# cors
CORS(app, supports_credentials=True)

# user reloader and db migrate
import models
@login_manager.user_loader
def load_user(user_id):
    user_obj = models.User.query.get(int(user_id))
    return user_obj


if __name__ == '__main__':

    # 开始日志
    ConfigLog()

    # development
    app.run(host='0.0.0.0', port=5996, debug=True)

