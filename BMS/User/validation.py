# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: validation.py
# @time: 19-6-25 上午11:07

# form validation
from wtforms import Form, StringField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from manage import images


class UserRegisterForm(Form):

    user_name = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !')
        ]
    )
    password = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !')
        ]
    )
    password2 = StringField(
        validators=[
            EqualTo('password', message="两次密码不一致")
        ]
    )

    @property
    def save_column(self):
        return [i for i in UserRegisterForm.__dict__.keys() if i != 'meta' and not i.startswith('_')]


class UserLoginForm(Form):

    user_name = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !')
        ]
    )
    password = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !')
        ]
    )

    @property
    def save_column(self):
        return [i for i in UserLoginForm.__dict__.keys() if i != 'meta' and not i.startswith('_')]


class AvatarUploadForm(Form):
    """verify upload data"""

    file = FileField(
        validators=[
            FileRequired(message='please select file !'),
            FileAllowed(images, message='only allowed to upload images !')
        ]
    )
