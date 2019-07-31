# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: websocket_client.py
# @time: 19-7-24 下午3:57


import websocket


def on_message(ws, message):
    print(ws)
    print(message)


def on_error(ws, error):
    print(ws)
    print(error)


def on_close(ws):
    print(ws)
    print("### closed ###")


websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    # "ws://192.168.2.179:8088/api/v1/hello",
    "ws://192.168.2.179:8089/chat",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close)

ws.run_forever()
