# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: crawl_server.py
# @time: 19-7-18 下午4:35


from flask_pymongo import DESCENDING
from flask import request, jsonify, make_response

from . import data_show_blue
from DataShow.validation import DataShowPaginateForm
from manage import mongo_bids


@data_show_blue.route('/api/v1/data_show')
def data_show():
    """
    show data
    :return:
    """

    # verification
    args_form = DataShowPaginateForm(request.args)
    if not args_form.validate():
        return make_response(jsonify({'results': args_form.errors}), 400)

    # through verification and then get params
    limit_params = int(request.args['limit'])
    offset_params = int(request.args['offset'])

    # query data and paginator
    data_show_list = mongo_bids.db.bids_info.find({}, {'bids_id': 0}).limit(
        limit_params).skip(offset_params).sort('bids_date', DESCENDING)

    results = []
    for record in data_show_list:
        record['_id'] = str(record['_id'])
        results.append(record)

    # statistic of count
    bids_total_count = mongo_bids.db.bids_info.count()

    return make_response(jsonify({
        'results': results,
        'bids_total_count': bids_total_count
    }), 200)


@data_show_blue.route('/api/v1/statistics')
def data_show_statistics():

    # bids region/result/date groupby statistic info
    bids_region_group_statistic = mongo_bids.db.bids_info.aggregate(
        [{
            '$group': {
                '_id': '$bids_region',
                'total_count': {'$sum': 1}
            }
        }]
    )
    bids_result_group_statistic = mongo_bids.db.bids_info.aggregate(
        [{
            '$group': {
                '_id': '$bids_result',
                'total_count': {'$sum': 1}
            }
        }]
    )
    bids_date_group_statistic = mongo_bids.db.bids_info.aggregate(
        [{
            '$group': {
                '_id': '$bids_date',
                'total_count': {'$sum': 1}
            }
        }]
    )

    # statistic of count
    bids_total_count = mongo_bids.db.bids_info.count()

    return make_response(jsonify({
        'bids_total_count': bids_total_count,
        'bids_region_group': list(bids_region_group_statistic),
        'bids_result_group': list(bids_result_group_statistic),
        'bids_date_group': list(bids_date_group_statistic)
    }), 200)


@data_show_blue.route('/api/v1/data_show/search')
def data_show_search():
    """
    search data
    :return:
    """

    # verification
    args_form = DataShowPaginateForm(request.args)
    if not args_form.validate():
        return make_response(jsonify({'results': args_form.errors}), 400)

    # through verification and then get params
    limit_params = int(request.args['limit'])
    offset_params = int(request.args['offset'])
    title_params = request.args.get('title', '')
    region_params = request.args.get('region', '')
    result_params = request.args.get('result', '')
    date_params = request.args.get('date', '')

    # search info and paginator
    search_list_paginator = mongo_bids.db.bids_info.find(
        {
            'bids_title': {'$regex': title_params, '$options': '$i'},  # ignore case
            'bids_region': {'$regex': region_params},
            'bids_result': {'$regex': result_params},
            'bids_date': {'$regex': date_params}
        },
        {'bids_id': 0}
    ).limit(limit_params).skip(offset_params).sort('bids_date', DESCENDING)

    results = []
    for record in search_list_paginator:
        record['_id'] = str(record['_id'])
        results.append(record)

    # statistic of count
    bids_total_count = mongo_bids.db.bids_info.find(
        {
            'bids_title': {'$regex': title_params, '$options': '$i'},
            'bids_region': {'$regex': region_params},
            'bids_result': {'$regex': result_params},
            'bids_date': {'$regex': date_params}
        },
        {'bids_id': 0}
    ).count()

    return make_response(jsonify({
        'results': results,
        'bids_total_count': bids_total_count
    }), 200)
