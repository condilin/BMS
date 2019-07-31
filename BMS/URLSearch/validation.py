# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: validation.py
# @time: 19-6-25 上午11:07

# form validation
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Regexp, NumberRange, AnyOf, Optional, URL
from flask_wtf.file import FileField, FileAllowed, FileRequired
# import upload obj
from manage import files


class URLSearchPaginateForm(Form):
    """verify paginate form """

    limit = StringField(
        validators=[
            DataRequired(message='字段不能为空'),
            # use Regexp function, precondition is must be use StringField !
            Regexp(regex='[1-9]', message='字段必须为数值且不为0')
        ]
    )
    offset = StringField(
        validators=[
            DataRequired(message='字段不能为空'),
            # use Regexp function, precondition is must be use StringField !
            Regexp(regex='\d+', message='字段必须为数值')
        ]
    )


class URLSearchPostForm(Form):

    hospital_name = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !')
        ]
    )
    hospital_url = StringField(
        validators=[
            DataRequired(message='the column is not allowed null !'),
            # when require_tld=True, the domains must be include the top level domain
            # when verify the localhosts, set require_tld=False
            # URL(require_tld=True, message='Invalid URL, please input the correct url !')
        ]
    )

    @property
    def save_column(self):
        return [i for i in URLSearchPostForm.__dict__.keys() if i != 'meta' and not i.startswith('_')]


class FileUploadForm(Form):
    """verify upload data"""

    file = FileField(
        validators=[
            FileRequired(message='please select file !'),
            FileAllowed(files, message='only allowed to upload files!')
        ]
    )
