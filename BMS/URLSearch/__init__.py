# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: __init__.py.py
# @time: 19-7-18 下午4:28


from flask import Blueprint

# create blueprint obj
url_search_blue = Blueprint('url_search_blue', __name__)

from . import views
