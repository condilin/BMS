# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: __init__.py.py
# @time: 19-7-23 上午10:37


from flask import Blueprint

# create blueprint obj
user_blue = Blueprint('user_blue', __name__)

from . import views
