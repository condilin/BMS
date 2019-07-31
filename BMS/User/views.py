# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: crawl_server.py
# @time: 19-7-23 上午11:02


import os
from flask import request, jsonify, make_response, session
from flask_login import login_user, login_required, logout_user, current_user

from . import user_blue
from manage import db, images
from models import User
from .validation import UserRegisterForm, UserLoginForm, AvatarUploadForm


@user_blue.route('/api/v1/users/register', methods=['POST'])
def user_register():

    # verification
    post_form = UserRegisterForm(request.form)
    if not post_form.validate():
        return make_response(jsonify({'results': post_form.errors}), 400)

    # query user whether existed
    user = User.query.filter_by(user_name=request.form['user_name']).first()
    if user:
        return make_response(jsonify({
            'msg': 'user: {}, is already exited !'.format(request.form['user_name'])
        }), 400)

    try:
        # add user
        new_user = User()
        new_user.role_id = 1
        new_user.user_name = request.form['user_name']
        new_user.password = request.form['password']  # use sha256 algorithm to hash password

        # commit
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return make_response(jsonify({'msg': 'save to sqlite db error !'}), 500)

    return make_response(jsonify({'results': new_user.serilize_return}), 200)


@user_blue.route('/api/v1/users/login', methods=['POST'])
def user_login():

    # verification
    post_form = UserLoginForm(request.form)
    if not post_form.validate():
        return make_response(jsonify({'results': post_form.errors}), 400)

    # get user
    user = User.query.filter_by(user_name=request.form['user_name']).first()
    if not user or not user.verify_password(request.form['password']):
        return make_response(jsonify({'msg': 'user name or password error !'}), 400)

    # login
    login_user(user, remember=True)
    return make_response(jsonify({'results': user.serilize_return}), 200)


@user_blue.route('/api/v1/users/logout', methods=['POST'])
@login_required
def user_logout():
    logout_user()
    return make_response(jsonify({'msg': 'successful to logout!'}), 200)


@user_blue.route('/api/v1/users/avatar', methods=['POST'])
@login_required
def user_avatar():

    # verification form
    image_form = AvatarUploadForm(request.files)
    if not image_form.validate():
        return make_response(jsonify({'msg': image_form.errors}), 400)

    # get upload picture
    file = request.files.get('file')

    # save picture to local and get the picture url
    file_name = images.save(file)
    pic_url = images.url(file_name)

    # save to sqlite
    try:
        user = current_user
        user.avatar_url = os.path.basename(pic_url)

        # commit
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return make_response(jsonify({'msg': 'save to sqlite db error !'}), 500)

    return make_response(jsonify({'results': {
        'pic_url': os.path.basename(pic_url)
    }}), 201)
