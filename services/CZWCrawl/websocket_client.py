# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: websocket_client.py
# @time: 19-7-22 下午3:57


from websocket import create_connection


# 通过socket路由访问
ws = create_connection("ws://192.168.2.179:5022/api/v1/hello")
ws.send("Hello, linyk3")
# ws.send("run_crawl")
result = ws.recv()
print(result)
# ws.close()


