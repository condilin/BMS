# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: models.py
# @time: 19-7-23 上午10:37


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from manage import db


class Role(db.Model):

    __tablename__ = 'tb_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __str__(self):
        return 'Role is: {}'.format(self.name)


class User(db.Model, UserMixin):

    __tablename__ = 'tb_users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    avatar_url = db.Column(db.String(128))
    remote_addr = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('tb_roles.id'))

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return 'User is: {}'.format(self.user_name)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serilize_return(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_avatar': self.avatar_url,
            'role_id': self.role_id
        }

    @staticmethod
    def commond():
        return {
            'add': 'flask db migrate -m "table init"',
            'upgrade': 'flask db upgrade'
        }


