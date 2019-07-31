# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: wechat.py
# @time: 19-7-24 下午5:01


import logging
import json
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.websocket import WebSocketHandler

from tornado.options import define, options
define("port", default=8089, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/api/v1/chat", ChatHandler),
        ]
        settings = dict(
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class ChatHandler(WebSocketHandler):
    # 存储每一个人的信息
    users = []

    # 判断源origin，对于符合条件的请求源允许链接， 用于跨域访问
    def check_origin(self, origin):
        return True

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    # 连接建立后被调用，客户端建立链接后调用open。
    def open(self):

        print("new client opened===>")
        # 链接上后再进行存储用户信息，self 为每个连接服务器的客户端的对象
        self.users.append(self)
        for user in self.users:
            # 主动向客户端发送message消息，message可以是字符串或者字典。
            user.write_message(json.dumps(
                {'login_msg': '用户{}已进入群聊!'.format(self.request.remote_ip)},
                ensure_ascii=False
            ))

    # 客户端发送消息过来时服务器调用on_message
    def on_message(self, message):
        # 如果前端发的数据是字典，需要转一下
        # parsed = tornado.escape.json_decode(message)
        for user in self.users:
            # write_message的消息会被前端ws.onmessage方法接收
            user.write_message(json.dumps(
                {'ip': '{}'.format(self.request.remote_ip), 'message': '{}'.format(message)},
                ensure_ascii=False
            ))

    # 客户端断开链接调用on_close
    def on_close(self):

        print("new client closed===>")
        self.users.remove(self)
        for user in self.users:
            user.write_message(json.dumps(
                {'logout_msg': '用户{}已退出群聊!'.format(self.request.remote_ip)},
                ensure_ascii=False
            ))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
