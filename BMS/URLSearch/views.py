# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: crawl_server.py
# @time: 19-7-18 下午4:35


import time
import bson
import os
import logging
import pandas as pd
from flask import request, jsonify, make_response
from flask_pymongo import DESCENDING

from . import url_search_blue
from URLSearch.validation import URLSearchPaginateForm, URLSearchPostForm, FileUploadForm
from Base.utils.utils import save_to_db
from manage import mongo_bids, files


@url_search_blue.route('/api/v1/url_info', methods=['GET', 'POST', 'PUT', 'DELETE'])
def url_info():
    """
    show data
    :return:
    """

    if request.method == 'GET':
        # verification
        args_form = URLSearchPaginateForm(request.args)
        if not args_form.validate():
            return make_response(jsonify({'results': args_form.errors}), 400)

        # through verification and then get params
        limit_params = int(request.args['limit'])
        offset_params = int(request.args['offset'])

        # query data and paginator
        url_search_list = mongo_bids.db.url_info.find({}).limit(limit_params).skip(offset_params)

        results = []
        for record in url_search_list:
            record['_id'] = str(record['_id'])
            results.append(record)

        # statistic of count
        bids_total_count = mongo_bids.db.url_info.count()

        return make_response(jsonify({
            'results': results,
            'bids_total_count': bids_total_count
        }), 200)

    elif request.method == 'POST':
        # verification
        post_form = URLSearchPostForm(request.form)
        if not post_form.validate():
            return make_response(jsonify({'results': post_form.errors}), 400)

        # get params of forms
        form_data = request.form.to_dict()

        # save to mongodb
        form_data = {k: v for k, v in form_data.items() if k in post_form.save_column}
        # add create time and update time
        form_data.update({
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'update_time': time.strftime("%Y-%m-%d %H:%M:%S")
        })

        # select database verify the hospital name whether existed
        name_existed = mongo_bids.db.url_info.find_one({'hospital_name': form_data['hospital_name']})
        if name_existed:
            return make_response(jsonify(
                {'msg': 'the hospital_name {} already exists !'.format(form_data['hospital_name'])}
            ), 400)

        try:
            url_id = mongo_bids.db.url_info.insert(form_data)
        except Exception as e:
            logging.error(e, exc_info=True)
            return make_response(jsonify({'msg': 'save url info to db error !'}), 500)

        # select and return
        url_info = mongo_bids.db.url_info.find_one({'_id': url_id})
        url_info['_id'] = str(url_info['_id'])

        return make_response(jsonify({'results': url_info}), 201)

    elif request.method == 'PUT':
        # verification
        _id = request.args.get('id', None)
        if not _id:
            return make_response(jsonify({'msg': 'params error !'}), 400)

        # get json data
        update_form = request.get_json()

        # save to mongodb
        try:
            mongo_bids.db.url_info.update_one(
                {'_id': bson.ObjectId(_id)},
                {'$set': {
                    'hospital_name': update_form.get('hospital_name'),
                    'hospital_url': update_form.get('hospital_url'),
                    'update_time': time.strftime("%Y-%m-%d %H:%M:%S")
                }}
            )
        except Exception as e:
            logging.error(e, exc_info=True)
            return make_response(jsonify({'msg': 'id is not exist !'}), 400)

        # select and return
        url_info = mongo_bids.db.url_info.find_one({'_id': bson.ObjectId(_id)})
        url_info['_id'] = str(url_info['_id'])

        return make_response(jsonify({'results': url_info}), 200)

    elif request.method == 'DELETE':

        # verification
        _id = request.args.get('id', None)
        if not _id:
            return make_response(jsonify({'msg': 'params error !'}), 400)

        # delete
        result = mongo_bids.db.url_info.delete_one({'_id': bson.ObjectId(_id)})

        if result.deleted_count == 0:
            return make_response(jsonify({'msg': 'id is not exist !'}), 400)

        return make_response(jsonify({'msg': 'ok !'}), 204)


@url_search_blue.route('/api/v1/file_uploads', methods=['POST'])
def file_upload():
    """
    file upload
    :return:
    """

    # verification form
    file_form = FileUploadForm(request.files)
    if not file_form.validate():
        return make_response(jsonify({'msg': file_form.errors}), 400)

    # get upload picture and save file to dst directory
    file = request.files.get('file')

    # save picture to local and get the picture url
    file_name = files.save(file)
    file_url = files.url(file_name)

    # verify the data columns whether satisfy
    _, suffix = os.path.splitext(file_url)
    data = pd.read_excel(file_url) if suffix in ['.xls', '.xlsx'] else pd.read_csv(file_url)
    if len(data.columns) != 2:
        return make_response(jsonify({'msg': 'data format is not satisfy, need 2 columns'}), 400)
    else:
        data.columns = ['hospital_name', 'hospital_url']

    # save to mongodb
    save_to_db(data, file_url, source_file_delete=False)

    return make_response(jsonify({'msg': 'successful to upload the file'}), 201)


@url_search_blue.route('/api/v1/url_info/search')
def url_info_search():
    """
    search data
    :return:
    """

    # verification
    args_form = URLSearchPaginateForm(request.args)
    if not args_form.validate():
        return make_response(jsonify({'results': args_form.errors}), 400)

    # through verification and then get params
    limit_params = int(request.args['limit'])
    offset_params = int(request.args['offset'])
    hospital_name_params = request.args.get('hospital_name', '')

    # search info and paginator
    search_list_paginator = mongo_bids.db.url_info.find(
        {
            'hospital_name': {'$regex': hospital_name_params}
        }
    ).limit(limit_params).skip(offset_params).sort('update_time', DESCENDING)

    results = []
    for record in search_list_paginator:
        record['_id'] = str(record['_id'])
        results.append(record)

    # statistic of count
    url_info_total_count = mongo_bids.db.url_info.find(
        {
            'hospital_name': {'$regex': hospital_name_params}
        },
        {'bids_id': 0}
    ).count()

    return make_response(jsonify({
        'results': results,
        'bids_total_count': url_info_total_count
    }), 200)
