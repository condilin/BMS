# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: tornado_websocket.py
# @time: 19-7-24 下午3:46


import time
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
import tornado.ioloop

from CZWCrawl.Crawl import CZWCrawler
from CZWCrawl.config.config import cfg
# init crawl object
czw_crawl = CZWCrawler(cfg.params_dict)


class WebSocketCrawlHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message('current time is {} ! your ip is {}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S"), self.request.remote_ip))

    def on_message(self, message):

        if message == 'run_crawl':
            self.write_message('爬虫程序正在启动.... please wait 2s...')
            time.sleep(2)
            self.write_message('爬虫程序启动成功！开始爬取！')
            czw_crawl.run(ws=self, message=message)
        elif message.lower() == 'ok':
            pass
        else:
            self.write_message('Hello {}, Welcome to use this system ! Please click button to start !'.format(message))

    def on_close(self):
        print("WebSocket closed !")


class App(Application):
    def __init__(self):
        handlers = [
            (r'/api/v1/hello', WebSocketCrawlHandler)
        ]

        settings = {'debug': True}
        Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = App()
    server = HTTPServer(ws_app)
    server.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
