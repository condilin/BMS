# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: validation.py
# @time: 19-6-25 上午11:07

# form validation
from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired, Regexp, NumberRange, AnyOf, Optional


class DataShowPaginateForm(Form):
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
    title = StringField(
        validators=[
            Optional()
        ]
    )
    region = StringField(
        validators=[
            Optional()
        ]
    )
    result = StringField(
        validators=[
            Optional()
        ]
    )
    date = StringField(
        validators=[
            Optional()
        ]
    )
