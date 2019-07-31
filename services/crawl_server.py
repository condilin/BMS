# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: crawl_server.py
# @time: 19-7-22 下午2:44


import time
from flask import Flask
from flask_sockets import Sockets
from geventwebsocket import WebSocketError

from CZWCrawl.Crawl import CZWCrawler
from CZWCrawl.config.config import cfg

app = Flask(__name__)
sockets = Sockets(app)

# init crawl object
czw_crawl = CZWCrawler(cfg.params_dict)


# websocket url
@sockets.route('/api/v1/websocket/crawl')
def echo_socket(ws):
    while not ws.closed:
        try:
            ws.send('current time is {} !'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            current_user = ws.receive()
            ws.send('Hello {}, Welcome to use this system ! Please click button to start !'.format(current_user))

            # receive message
            crawl_status = ws.receive()
            if crawl_status == 'run_crawl':
                ws.send('爬虫程序已启动, 正在执行中.... please wait 2s...')
                time.sleep(2)
                czw_crawl.run(ws)
            else:
                ws.send("come from web server: " + str(crawl_status))
        except WebSocketError as e:
            continue


if __name__ == "__main__":
    import sys
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    # development
    server = pywsgi.WSGIServer(('', 5022), app, handler_class=WebSocketHandler)
    print('server start...')
    server.serve_forever()

    # product
    # port = sys.argv[1]
    # try:
    #     port = int(port)
    # except:
    #     raise Exception("PORT %s IS NOT ACCEPTED!" % port)
    #
    # server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    # print('server start...')
    # server.serve_forever()
