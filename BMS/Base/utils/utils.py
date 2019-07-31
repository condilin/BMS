# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: utils.py
# @time: 19-7-19 上午10:01


import time
import os
import functools
from threading import Thread
from manage import mongo_bids


def asynchronous_task(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


@asynchronous_task
def save_to_db(data, file_url, source_file_delete=False):

    # save to mongodb and add create time
    for _, row in data.iterrows():
        row_val = row.to_dict()
        # can use datetime module to transform the type of string to type of datetime, so can calculate interval
        row_val.update({
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'update_time': time.strftime("%Y-%m-%d %H:%M:%S")
        })

        # TODO: verify hospital url

        # save to db
        mongo_bids.db.url_info.insert(row_val)

    # remove uploaded file
    if source_file_delete:
        os.remove(file_url)
